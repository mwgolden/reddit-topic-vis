import os
import json
import yaml
import awswrangler as wr
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

import logging

logger = logging.getLogger()
logger.setLevel("INFO")


sql = """
    WITH latest AS (
        SELECT
            post_id,
            max(hive_partition_date) AS most_recent_download
        FROM "reddit.bronze".comments
        GROUP BY post_id
    )
    SELECT
        c.post_id,
        c.run_date,
        c.data
    FROM "reddit.bronze".comments c
    JOIN latest l
    ON c.post_id = l.post_id
    AND c.hive_partition_date = l.most_recent_download
    WHERE c.post_id = ?
"""

OUTPUT_PATH = "s3://com.wgolden.reddit/silver/comments"
READ_TABLE = "comments"

DATABASE = "reddit.silver"
COMMENTS_TABLE = "comments"

BASE_DIR = Path(__file__).parent

def load_dtype(relative_path:str) -> dict[str, str]:
    path = BASE_DIR / relative_path
    with open(path, "r") as f:
        schema = yaml.safe_load(f)
    return schema["columns"]

def lambda_handler(event, context):

    logger.info(event)
    event_detail = event.get("detail", {})
    if not event_detail:
        logger.warning("Detail object is empty")
        logger.warning("## Event Object ##")
        logger.warning(event_detail)

    else:
        post_id = event_detail.get("post_id", None)

    

        run_date = datetime.now(timezone.utc)
        timestamp_str = run_date.strftime("%Y-%m-%d %H:%M:%S")
        hive_partition_date_str = run_date.strftime("%Y-%m-%d")

        schema = load_dtype("schemas/comments.yaml")
        columns = list(schema.keys())
        
        comments_df = wr.athena.read_sql_query(
            sql=sql,
            database=DATABASE,
            paramstyle="qmark",
            params=[post_id],
            s3_output="s3://com.wgolden.reddit/silver/temp"
        )

        comments_df["data_json"] = comments_df["data"].map(json.loads)

        logger.info(
            "Dataframe shape=%s columns=%s",
            comments_df.shape,
            list(comments_df.columns)
        )

        logger.info("### Normalize Comments ###")
        comments_normalized = pd.json_normalize(comments_df["data_json"].to_list(), max_level=0) # to_list() isn't necessary, but prevents pylance from complaining
        
        # Any columns not in the columns list
        extra_columns = set(comments_normalized.columns) - set(columns)
        comments_normalized["extra_columns"] = comments_normalized[list(extra_columns)].to_dict(orient="records")
        comments_normalized = comments_normalized.reindex(columns=columns)
        # save media_metadata as proper json string
        comments_normalized["media_metadata"] = comments_normalized["media_metadata"].apply(
            lambda x: json.dumps(x) if isinstance(x, (dict, list)) else None
        )
        comments_normalized = comments_normalized.assign(
            post_id=comments_df["post_id"].values,
            ingested_at=comments_df["run_date"].values,
            normalized_at=timestamp_str,
            hive_partition_date=hive_partition_date_str
        )
        
        logger.info(
            "Dataframe shape=%s columns=%s",
            comments_normalized.shape,
            list(comments_normalized.columns)
        )

        logger.info("### Write to data catalog ###")
        
        wr.catalog.create_database(
            name=DATABASE, 
            description="reddit data silver layer",
            exist_ok=True
        )

        logger.info(f"Write comments dataframe to silver layer: {OUTPUT_PATH}/hive_partition_date={hive_partition_date_str}/post_id={post_id}")
        wr.s3.to_parquet(
            df=comments_normalized,
            dataset=True,
            path=OUTPUT_PATH,
            partition_cols=["hive_partition_date", "post_id"],
            database=DATABASE,
            table=COMMENTS_TABLE,
            mode="overwrite_partitions",
            dtype=schema,
            use_threads=False
        )


if __name__ == "__main__":

    event = {
        "version": "0",
        "id": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
        "detail-type": "MyCustomEvent",
        "source": "my.app",
        "account": "123456789012",
        "time": "2026-01-30T15:04:05Z",
        "region": "us-east-1",
        "resources": [],
        "detail": {"bot_name": "reddit_bot", "post_id": "1qqzp06"}
    }

    lambda_handler(event=event, context=None)