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

SQL = """
with recursive comment_tree(
    post_id
    ,comment_id
    ,parent_id
    ,author
    ,comment
    ,path
    ,depth
    ,normalized_at
) as (
    SELECT 
        post_id
        ,concat('t1_', id) AS comment_id
        ,parent_id
        ,author
        ,body AS comment
        ,array[concat('t1_', id)] AS path
        ,1 AS depth
        ,normalized_at
    FROM "reddit.silver".comments c
    WHERE post_id = ?
      AND parent_id LIKE 't3_%'
      AND hive_partition_date = (
          SELECT max(hive_partition_date) 
          FROM "reddit.silver".comments
          WHERE post_id = ?
            AND post_id = c.post_id
      )
    UNION ALL
    SELECT 
        t.post_id
        ,concat('t1_', c.id) AS comment_id
        ,c.parent_id
        ,c.author
        ,c.body AS comment
        ,t.path || array[concat('t1_', c.id)] AS path
        ,t.depth + 1 AS depth
        ,t.normalized_at
    FROM comment_tree t
    JOIN "reddit.silver".comments c
      ON c.parent_id = t.comment_id
     and t.post_id = ? 
     and hive_partition_date = (
          SELECT max(hive_partition_date) 
          FROM "reddit.silver".comments
          WHERE post_id = ?
            AND post_id = c.post_id
      )
)      
select 
    post_id
    ,parent_id
    ,comment_id
    ,depth
    ,CONCAT('[', array_join(transform(path, x -> CONCAT('"', x, '"')), ','), ']') AS path
    ,author
    ,comment
    ,normalized_at
from comment_tree
"""

DATABASE = "reddit.gold"
BASE_DIR = Path(__file__).parent
OUTPUT_PATH = "s3://com.wgolden.reddit/gold/comment_hierarchy"
WF_TABLE = "reddit_comment_hierarchy"


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
        
        comment_hierarchy_df = wr.athena.read_sql_query(
            sql=SQL,
            database=DATABASE,
            paramstyle="qmark",
            params=[post_id, post_id, post_id, post_id],
            s3_output="s3://com.wgolden.reddit/gold/temp"
        )

        
        comment_hierarchy_df = comment_hierarchy_df.assign(
            run_tmstmp=timestamp_str
        )

        logger.info(
            "Dataframe shape=%s columns=%s",
            comment_hierarchy_df.shape,
            list(comment_hierarchy_df.columns)
        )
        
        logger.info("### Write to data catalog ###")
        logger.info(f"Write comment hierarchy to gold layer: {OUTPUT_PATH}/post_id={post_id}")
        wr.s3.to_parquet(
            df=comment_hierarchy_df,
            dataset=True,
            path=OUTPUT_PATH,
            partition_cols=["post_id"],
            database=DATABASE,
            table=WF_TABLE,
            mode="overwrite_partitions",
            dtype={"post_id": "string", "comment_id": "string", "parent_id": "string", "comment": "string", "path": "string", "depth": "int", "normalized_at": "timestamp", "run_tmstmp": "timestamp"},
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