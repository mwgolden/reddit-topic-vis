import logging
import json
import boto3
from datasets.comment_tree import publish_comment_tree
from datasets.word_freq import publish_word_counts

logger = logging.getLogger()
logger. setLevel("INFO")

PUBLISH_BUCKET = "com.wgolden.reddit-public-data"
STAGING_PREFIX = "datasets/build"

s3_client = boto3.client("s3")

def write_data_to_tmp(data, file_name):
    with open(f"/tmp/{file_name}.json", "w") as f:
            json.dump(data, f, indent=2)

def lambda_handler(event, context):
    logger.info(f"Event: {event}")

    data, file_name = None, None
    post_id = event.get("post_id", None)
    dataset = event.get("dataset", None)
    build_id = event.get("build_id", None)

    logger.info(f"Publish {dataset} for {post_id}")
    if dataset == "comment_tree" and post_id:
        data = publish_comment_tree(post_id)
        file_name = f"{post_id}_comment_tree"
    elif dataset == "word_frequency" and post_id:
         data = publish_word_counts(post_id)
         file_name = f"{post_id}_word_freq"

    if data and file_name:
        write_data_to_tmp(data, file_name)
        source_path = f"/tmp/{file_name}.json"
        dest_key = f"{STAGING_PREFIX}/{post_id}/{build_id}/{file_name}.json"
        s3_client.upload_file(source_path, PUBLISH_BUCKET, dest_key)


if __name__ == "__main__":

    event = {
        "dataset": "comment_tree", 
        "post_id": "1qxc496", 
        "build_id": "2026-02-08T12-50-46Z"
    }

    lambda_handler(event=event, context=None)