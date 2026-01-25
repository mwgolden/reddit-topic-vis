import json
import boto3
import math
import os
import urllib3
from api_token_cache import http_requests
from api_token_cache.models import DynamoDbConfig

ENDPOINT = os.environ.get('API_ENDPOINT')
BUCKET = os.environ.get('S3_BUCKET')
QUEUE_URL = os.environ.get('QUEUE_URL')

def get_more_comment_ids(listings):
    more_comments_ids = []
    for listing in listings:
        children = listing.get("data", {}).get("children", [])
        for child in children:
            if child.get("kind") == "more":
                more_comments_ids.extend(child["data"]["children"])

    return more_comments_ids


def save_to_bucket(json_object, key):    
    s3 = boto3.resource("s3")
    obj = s3.Object(BUCKET, key) # type: ignore
    response = obj.put(Body=json.dumps(json_object))
    return response


def queue_more_comments(post_id, message, queue_url):
    sqs_client = boto3.client('sqs')
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
        MessageGroupId=post_id
    )
    print(response)

def process_more_comments(comment_ids, post_id, more_comments_key, bot_name, queue_url):
    total_pages = math.ceil(len(comment_ids) / 100)
    page = 0
    for i in range(0, total_pages):
        start = i * 100
        stop = start + 100
        page = i + 1
        msg = {
            "bot_name": bot_name,
            "post_id": post_id,
            "start": start,
            "stop": stop,
            "s3_bucket": BUCKET,
            "bucket_key": more_comments_key,
            "page": page,
            "total_pages": total_pages,
            "status": "downloading",
            "queue_url": queue_url
        }
        queue_more_comments(post_id, msg, queue_url)

def lambda_handler(event, context):
    bot_name = event['bot_name']
    post_id = event['post_id']  
    url = f'{ENDPOINT}/{post_id}?threaded=False'

    db_config = DynamoDbConfig(api_config_table="api_bot_config", api_token_cache_table="api_token_cache")
    http_pool = urllib3.PoolManager()

    listings = http_requests.http_oauth_client_credentials(url=url, bot_name=bot_name, db_config=db_config, http=http_pool)


    bucket_key = f'raw/comments/{post_id}/0_{post_id}.json'
    save_to_bucket(listings, bucket_key)
    more_comments = get_more_comment_ids(listings)
    if more_comments:
        more_comments_key = f'raw/comments_cache/{post_id}_more_comments.json'
        save_to_bucket(more_comments, more_comments_key)
        process_more_comments(more_comments, post_id, more_comments_key, bot_name, QUEUE_URL)

    return {
        "statusCode": 200,
        "body": ""
    }

if __name__ == "__main__":
    event = {
        "bot_name": "reddit_bot",
        "post_id": "1qgyjdg"
    }
    lambda_handler(event=event, context=None)