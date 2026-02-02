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
        FROM posts
        GROUP BY post_id
    )
    SELECT
        c.post_id,
        c.run_date,
        c.data
    FROM posts c
    JOIN latest l
    ON c.post_id = l.post_id
    AND c.hive_partition_date = l.most_recent_download
    WHERE c.post_id = ?
"""

OUTPUT_PATH = "s3://com.wgolden.reddit/silver/posts"
READ_DATABASE = "reddit.bronze"
READ_TABLE = "posts"

WRITE_DATABASE = "reddit.silver"
POSTS_TABLE = "posts"

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

        schema = load_dtype("schemas/posts.yaml")
        columns = list(schema.keys())
        
        posts_df = wr.athena.read_sql_query(
            sql=sql,
            database=READ_DATABASE,
            paramstyle="qmark",
            params=[post_id]
        )

        posts_df["data_json"] = posts_df["data"].map(json.loads)

        logger.info(
            "Dataframe shape=%s columns=%s",
            posts_df.shape,
            list(posts_df.columns)
        )

        logger.info("### Normalize posts ###")
        posts_normalized = pd.json_normalize(posts_df["data_json"].to_list(), max_level=0) # to_list() isn't necessary, but prevents pylance from complaining
        
        # Any columns not in the columns list
        extra_columns = set(posts_normalized.columns) - set(columns)
        posts_normalized["extra_columns"] = posts_normalized[list(extra_columns)].to_dict(orient="records")
        posts_normalized = posts_normalized.reindex(columns=columns)

        # save media_metadata as proper json string
        posts_normalized["media_metadata"] = posts_normalized["media_metadata"].apply(
            lambda x: json.dumps(x) if isinstance(x, (dict, list)) else None
        )

        posts_normalized = posts_normalized.assign(
            post_id=posts_df["post_id"].values,
            ingested_at=posts_df["run_date"].values,
            normalized_at=timestamp_str,
            hive_partition_date=hive_partition_date_str
        )
        
        logger.info(
            "Dataframe shape=%s columns=%s",
            posts_normalized.shape,
            list(posts_normalized.columns)
        )
        
        logger.info("### Write to data catalog ###")
        
        wr.catalog.create_database(
            name=WRITE_DATABASE, 
            description="reddit data silver layer",
            exist_ok=True
        )
        
        logger.info(f"Write posts dataframe to silver layer: {OUTPUT_PATH}/hive_partition_date={hive_partition_date_str}/post_id={post_id}")
        wr.s3.to_parquet(
            df=posts_normalized,
            dataset=True,
            path=OUTPUT_PATH,
            partition_cols=["hive_partition_date", "post_id"],
            database=WRITE_DATABASE,
            table=POSTS_TABLE,
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