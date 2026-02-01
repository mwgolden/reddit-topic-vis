import os
import json
import boto3
import pandas as pd
import awswrangler as wr
from datetime import datetime, timezone
from typing import Dict, List

import logging

logger = logging.getLogger()
logger.setLevel("INFO")

s3_client = boto3.client("s3")


def sort_keys(file_keys: List[str]) -> List[str]:
    sorted_file_keys = []
    try:
        sorted_file_keys = sorted(file_keys, key=lambda x: int(x.split('/')[-1].split('_')[0]))
    except Exception as e:
        logger.error("Unable to sort file keys: {e}")

    return sorted_file_keys


def post_from_first_file(bucket: str, prefix: str) -> List[Dict]:
    data = s3_client.get_object(Bucket=bucket, Key=prefix)
    contents = data["Body"].read()
    json_data = json.loads(contents.decode("utf-8"))
    post_meta = []
    for item in json_data:
        for child in item.get("data", {}).get("children", []):
            if child.get("kind", None) == "t3":
                post_meta.append(child)
    
    return post_meta


BUCKET = "com.wgolden.reddit"
POST_PREFIX = """raw/comments/{post_id}/"""

OUTPUT_PATH = "s3://com.wgolden.reddit/bronze/posts"
DATABASE = "reddit.bronze"
TABLE = "posts"

def lambda_handler(event, context):

    event_detail = event.get("detail", {})
    if not event_detail:
        logger.warning("Detail object is empty")
        logger.warning("## Event Object ##")
        logger.warning(event_detail)

    else: 
        post_id = event_detail["post_id"]
        bucket_prefix = POST_PREFIX.format(post_id=post_id)
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=BUCKET, Prefix=bucket_prefix)
        object_prefixes = sort_keys(
            [obj["Key"] 
            for page in pages
            for obj in page.get("Contents", [])]
        )
        post = post_from_first_file(bucket=BUCKET, prefix=object_prefixes[0])
        logger.info(f"Processed {len(post)} items from first file")

        run_date = datetime.now(timezone.utc)
        timestamp_str = run_date.strftime("%Y-%m-%d %H:%M:%S")
        hive_partition_date_str = run_date.strftime("%Y-%m-%d")
        df = pd.DataFrame(data=post)
        df["data"] = df["data"].apply(lambda x: json.dumps(x))
        df["post_id"] = post_id
        df["run_date"] = timestamp_str
        df["hive_partition_date"] = hive_partition_date_str

        logger.info(
            "Dataframe shape=%s columns=%s",
            df.shape,
            list(df.columns)
        )
        
        wr.catalog.create_database(
            name=DATABASE, 
            description="reddit data bronze layer",
            exist_ok=True
        )

        logger.info(f"Write posts dataframe to bronze layer: {OUTPUT_PATH}/hive_partition_date={hive_partition_date_str}/post_id={post_id}")
        wr.s3.to_parquet(
            df=df,
            dataset=True,
            path=OUTPUT_PATH,
            partition_cols=["hive_partition_date", "post_id"],
            database=DATABASE,
            table=TABLE,
            mode="overwrite_partitions",
            dtype={"data": "string"},
            use_threads=False
        )
    
    return {
        "statusCode": 200,
        "body": ''
    }


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
        "detail": {"bot_name": "reddit_bot", "post_id": "1qqzp06", "status": "complete", "queue_url": "https://sqs.<region>.amazonaws.com/<acct_id>/queue.fifo"}
    }

    lambda_handler(event=event, context=None)