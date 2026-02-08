import logging
import json
import awswrangler as wr
import pandas as pd
from typing import Dict

logger = logging.getLogger()
logger. setLevel("INFO")

SQL = """
    select token, wc 
    from "reddit.gold".reddit_post_word_frequency
    where post_id = ?
"""

def publish_word_counts(post_id: str) -> Dict:
    logger.info(f"Build word frequency table for {post_id}")
    wf_table = wr.athena.read_sql_query(
        sql=SQL,
        database="reddit.gold",
        paramstyle="qmark",
        params=[post_id],
        s3_output="s3://com.wgolden.reddit/gold/temp"
    )
    word_frequencies = wf_table.set_index("token")["wc"].to_dict()
    return word_frequencies