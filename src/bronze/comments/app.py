import json
import boto3
import pandas as pd
import awswrangler as wr
from datetime import datetime

s3_client = boto3.client("s3")


def sort_keys(file_keys: list[str]) -> list[str]:
    sorted_file_keys = sorted(file_keys, key=lambda x: int(x.split('/')[-1].split('_')[0]))
    return sorted_file_keys



def lambda_handler(event, context):

    post_id = "1qgyjdg"
    path = f"s3://com.wgolden.reddit/raw/comments/{post_id}/"

    response = s3_client.list_objects_v2(Bucket="com.wgolden.reddit", Prefix=f"raw/comments/{post_id}/")
    object_keys = sort_keys([obj["Key"] for obj in response["Contents"]])
    print(object_keys)

    data = s3_client.get_object(Bucket="com.wgolden.reddit", Key=object_keys[0])
    contents = data["Body"].read()
    json_data = json.loads(contents.decode("utf-8"))

    t1 = [item for item in json_data[1]["data"]["children"] if item["kind"] == "t1"]
    print(len(t1))

    object_keys.pop(0)

    more_comments = []
    for key in object_keys:
        data = s3_client.get_object(Bucket="com.wgolden.reddit", Key=key)
        contents = data["Body"].read()
        json_data = json.loads(contents.decode("utf-8"))
        comments = [item for item in json_data["json"]["data"]["things"] if item["kind"] == "t1"]
        more_comments.extend(comments)
    print(len(more_comments))

    t1.extend(more_comments)

    print(len(t1))
    run_date = datetime.now()
    timestamp_str = run_date.strftime("%Y-%m-%d %H:%M:%S")
    hive_partition_date_str = run_date.strftime("%Y-%m-%d")
    df = pd.DataFrame(data=t1)
    df["post_id"] = post_id
    df["run_date"] = timestamp_str
    df["hive_partition_date"] = hive_partition_date_str
    print(df)

    wr.catalog.create_database(
        name="reddit.bronze", 
        description="reddit data bronze layer",
        exist_ok=True
    )

    wr.s3.to_parquet(
        df=df,
        dataset=True,
        path="s3://com.wgolden.reddit/bronze/comments/",
        partition_cols=["hive_partition_date", "post_id"],
        database="reddit.bronze",
        table="comments",
        mode="overwrite_partitions",
        dtype={"data": "string"}
    )
    



if __name__ == "__main__":
    lambda_handler(event=None, context=None)