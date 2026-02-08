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

def publish_comment_tree(post_id: str) -> Dict:
    logger.info(f"Build comment tree for {post_id}")
    df = wr.athena.read_sql_query(
        sql=SQL,
        database="reddit.gold",
        paramstyle="qmark",
        params=[post_id],
        s3_output="s3://com.wgolden.reddit/gold/temp"
    )
    
    comment_tree = build_comment_tree(df)
    return comment_tree