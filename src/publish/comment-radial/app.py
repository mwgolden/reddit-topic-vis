import logging
import json
import awswrangler as wr
import pandas as pd
from typing import Dict


logger = logging.getLogger()
logger. setLevel("INFO")

SQL = """
select * from "reddit.gold".reddit_comment_hierarchy where post_id = ? order by depth
"""

def build_comment_tree(df: pd.DataFrame) -> Dict:
    tree = {"name": df["parent_id"].iloc[0], "children": []}

    for _, row in df.iterrows():
        path = json.loads(row["path"])
        parent = tree
        for i, cid in enumerate(path):
            if i == 0: 
                # top level comment
                parent_children = parent.setdefault("children", [])
                # check if already exists
                node = next((c for c in parent_children if c["name"] == cid), None)
                if not node:
                    node = {"name": cid, "body": row["comment"], "author": row["author"], "children": []}
                    parent_children.append(node)
                parent = node
            else: 
                parent_children = parent["children"]
                node = next((c for c in parent_children if c["name"] == cid), None)
                if not node: 
                    node = {"name": cid, "body": row["comment"], "author": row["author"], "children": []}
                    parent_children.append(node)
                parent = node
    return tree

def lambda_handler(event, context):
    logger.info(f"Event: {event}")
    event_detail = event.get("detail", {})
    if not event_detail:
        logger.warning("Detail object is empty")
        logger.warning("## Event Object ##")
        logger.warning(event_detail)
    else:
        post_id = event_detail.get("post_id", None)
        df = wr.athena.read_sql_query(
            sql=SQL,
            database="reddit.gold",
            paramstyle="qmark",

            params=[post_id],
            s3_output="s3://com.wgolden.reddit/gold/temp"
        )
        
        comment_tree = build_comment_tree(df)

        with open("reddit_comment_tree.json", "w") as f:
            json.dump(comment_tree, f, indent=2)





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