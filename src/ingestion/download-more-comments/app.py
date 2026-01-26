import boto3
import json
import os
import urllib3
from api_token_cache import http_requests
from api_token_cache.models import DynamoDbConfig


ENDPOINT = os.environ.get('API_ENDPOINT')
BUCKET = os.environ.get('S3_BUCKET')

def emit_download_complete_event(event_payload):
    # Will use the default event bus
    event_bridge_client = boto3.client('events')
    response = event_bridge_client.put_events(
        Entries=[{
            "DetailType": "Reddit Comment Download Complete",
            "Source": "reddit.ingestion",
            "Detail": json.dumps(event_payload)
        }]
    )
    print(response)

def save_to_bucket(json_object, key):    
    s3 = boto3.resource("s3")
    obj = s3.Object(BUCKET, key) # type: ignore
    response = obj.put(Body=json.dumps(json_object))
    return response

def get_from_bucket(bucket, key):
    s3 = boto3.client('s3')
    file_obj = s3.get_object(Bucket=bucket,Key=key)
    fileData = file_obj['Body'].read()
    return json.loads(fileData)


def lambda_handler(event, context):

    db_config = DynamoDbConfig(api_config_table="api_bot_config", api_token_cache_table="api_token_cache")
    http_pool = urllib3.PoolManager()

    records = event['Records']
    for record in records:
        message = json.loads(record['body'])
        post_id = message['post_id']
        if message["status"] == "complete":
            print(f"download complete for post {post_id}")
            emit_download_complete_event(message)
        else:
            bot_name = message['bot_name']
            s3_bucket = message['s3_bucket']
            bucket_key = message['bucket_key']
            start = message['start']
            stop = message['stop']
            total_pages = message['total_pages']
            page = message['page']
            comment_ids = get_from_bucket(s3_bucket, bucket_key)
            next_comments = comment_ids[start:stop]
            url = f'{ENDPOINT}?link_id=t3_{post_id}&morechildren={",".join(next_comments).replace(",","%2C")}&api_type=json'
            listings = http_requests.http_oauth_client_credentials(url=url, bot_name=bot_name, db_config=db_config, http=http_pool)
            res = save_to_bucket(json_object=listings, key=f'raw/comments/{post_id}/{page}_{post_id}.json')
    return {
        "statusCode": 200,
        "body": ''
    }