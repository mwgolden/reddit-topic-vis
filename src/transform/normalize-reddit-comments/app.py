import awswrangler as wr
import pandas as pd
from typing import Tuple


def sort_files(file_paths: list[str]) -> list[str]:
    sorted_file_paths = sorted(file_paths, key=lambda x: int(x.split('/')[-1].split('_')[0]))
    return sorted_file_paths

def process_first_file(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    wr.s3.read_json(file_path)

    raw_data = wr.s3.read_json(file_path)
    t3 = raw_data['data'][0]
    t1 = raw_data['data'][1]

    t3_df = pd.json_normalize(
        data=t3,
        record_path=["children"]
    )

    t1_df = pd.json_normalize(
        data=t1,
        record_path=["children"]
    )

    t1_df = t1_df[t1_df["kind"] == "t1"]

    return (t3_df, t1_df)

def process_remaining_files(file_paths: list[str]) -> pd.DataFrame:
    more_comments = wr.s3.read_json(path=file_paths)
    more_comments_df = pd.json_normalize(
        data=more_comments.to_dict(orient="records"),
        record_path=["json", "things"]
    )

    return more_comments_df

def lambda_handler(event, context):

    post_id = "1qgyjdg"
    path = f"s3://com.wgolden.reddit/raw/comments/{post_id}/"
    file_paths = wr.s3.list_objects(path)
    sorted_file_paths = sort_files(file_paths)
    first_file = sorted_file_paths.pop(0)
    
    submission_df, comments_df = process_first_file(file_path=first_file)

    more_comments_df = process_remaining_files(file_paths=sorted_file_paths)

    all_comments_df = pd.concat(
        [comments_df, more_comments_df],
        ignore_index=True,
        sort=False
    )

    print(all_comments_df.dtypes)

    wr.s3.to_parquet(
        submission_df,
        f"s3://com.wgolden.reddit/bronze/posts/post_id={post_id}",
        dataset=True,
        mode="overwrite_partitions",
        database="reddit",
        table="posts"
    )

    wr.s3.to_parquet(
        all_comments_df,
        f"s3://com.wgolden.reddit/bronze/comments/post_id={post_id}",
        dataset=True,
        mode="overwrite_partitions",
        database="reddit",
        table="comments"
    )

    



if __name__ == "__main__":
    lambda_handler(event=None, context=None)