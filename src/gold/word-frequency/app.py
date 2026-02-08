import logging
import os
import json
import awswrangler as wr
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from typing import List

logger = logging.getLogger()
logger.setLevel("INFO")

SQL = r"""
WITH latest AS (
        select
            post_id,
            max(hive_partition_date) AS most_recent_post
        from "reddit.silver".comments
        where post_id = ?
        group by post_id
    ),
cleaned as (
    select 
        c.post_id,
        -- keep apostrophes initially
        regexp_replace(lower(c.body), '[^A-Za-z0-9''\s_]', '') as body_keep_apostrophe,
        c.normalized_at
    FROM "reddit.silver".comments c
    join latest l on l.post_id = c.post_id
        and l.most_recent_post = c.hive_partition_date
),
comment_arrays as (
    select 
        post_id,
        -- remove apostrophes that are not inside words
        split(
            regexp_replace(body_keep_apostrophe, '(^|\s)''|''(\s|$)', ' '),
            ' '
        ) as comments,
        normalized_at
    from cleaned
)
select 
    post_id,  
    token,
    count(*) as wc 
    ,normalized_at
from comment_arrays
cross join unnest(comments) as t(token)
where length(token) > 2
group by normalized_at, post_id, token
order by wc desc
"""

DATABASE = "reddit.gold"
BASE_DIR = Path(__file__).parent
OUTPUT_PATH = "s3://com.wgolden.reddit/gold/post_word_frequency"
WF_TABLE = "reddit_post_word_frequency"

def stop_words(relative_path:str) -> List[str]:
    path = BASE_DIR / relative_path
    with open(path, "r") as f:
        stop_words = json.load(f)
    
    return stop_words["stop_words"]

def lambda_handler(event, context):
    logger.info(f"Event: {event}")
    event_detail = event.get("detail", {})
    if not event_detail:
        logger.warning("Detail object is empty")
        logger.warning("## Event Object ##")
        logger.warning(event_detail)

    else:
        # create database if not exists
        wr.catalog.create_database(
            name=DATABASE, 
            description="reddit data gold layer",
            exist_ok=True
        )


        post_id = event_detail.get("post_id", None)
        run_date = datetime.now(timezone.utc)
        timestamp_str = run_date.strftime("%Y-%m-%d %H:%M:%S")
        
        word_counts_df = wr.athena.read_sql_query(
            sql=SQL,
            database=DATABASE,
            paramstyle="qmark",
            params=[post_id],
            s3_output="s3://com.wgolden.reddit/gold/temp"
        )

        exclude_list = stop_words("stop_words.json")

        mask = word_counts_df["token"].isin(exclude_list)

        word_counts_filtered_df = word_counts_df[~mask]

        word_counts_filtered_df = word_counts_filtered_df.assign(
            run_tmstmp=timestamp_str
        )

        logger.info(
            "Dataframe shape=%s columns=%s",
            word_counts_filtered_df.shape,
            list(word_counts_filtered_df.columns)
        )
        
        logger.info("### Write to data catalog ###")
        logger.info(f"Write word frequencies to gold layer: {OUTPUT_PATH}/post_id={post_id}")
        wr.s3.to_parquet(
            df=word_counts_filtered_df,
            dataset=True,
            path=OUTPUT_PATH,
            partition_cols=["post_id"],
            database=DATABASE,
            table=WF_TABLE,
            mode="overwrite_partitions",
            dtype={"post_id": "string", "token": "string", "wc": "int", "run_tmstmp": "timestamp", "normalized_at": "timestamp"},
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
        "detail": {"bot_name": "reddit_bot", "post_id": "1qxc496"}
    }

    lambda_handler(event=event, context=None)