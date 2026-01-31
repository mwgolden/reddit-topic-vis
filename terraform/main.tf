
module "ingestion" {
  source = "./modules/ingestion"
  download_s3_arn = aws_s3_bucket.com_wgolden_reddit.arn
  api_token_cache_tables = var.api_token_cache_tables
  eventbridge_default_arn =  local.eventbridge_default_arn
  lambda_config = {
    "comments": {
        function_name = "reddit-ingestion-comments",
        archive_src_path = "../src/ingestion/download-reddit-comments",
        archive_build_path = "../build/download-reddit-comments.zip",
        lambda_handler = "app.lambda_handler",
        runtime = "python3.12",
        environment_variables = {
            "API_ENDPOINT": "https://oauth.reddit.com/comments",
            "S3_BUCKET": aws_s3_bucket.com_wgolden_reddit.id
        }
    },
    "more_comments": {
        function_name = "reddit-ingestion-more-comments",
        archive_src_path = "../src/ingestion/download-more-comments",
        archive_build_path = "../build/download-more-comments.zip",
        lambda_handler = "app.lambda_handler",
        runtime = "python3.12",
        environment_variables = {
            "API_ENDPOINT": "https://oauth.reddit.com/api/morechildren",
            "S3_BUCKET": aws_s3_bucket.com_wgolden_reddit.id
        }
    }
  }
}

module "bronze_layer" {
  source = "./modules/bronze_layer"
  region = local.region
  account_id = local.account_id
  data_bucket_name = var.data_bucket_name
  event_source_config = {
    eventbridge_default_arn = local.eventbridge_default_arn
    events = module.ingestion.ingestion_completion_event
  }
  data_catalog = {
    database_name = "reddit.bronze"
    tables = {
      comments_table = "comments"
      posts_table = "posts"
    }
  }
  lambda_config = {
    "posts": {  
        function_name = "reddit-bronze-posts"
        archive_src_path = "../src/bronze/posts"
        archive_build_path = "../build/reddit-bronze-posts.zip"
        lambda_handler = "app.lambda_handler",
        runtime = "python3.12",
        environment_variables = {
            
        }
    },
    "comments": {
        function_name = "reddit-bronze-comments"
        archive_src_path = "../src/bronze/comments"
        archive_build_path = "../build/reddit-bronze-comments.zip"
        lambda_handler = "app.lambda_handler",
        runtime = "python3.12",
        environment_variables = {
            
        }
    }
  }

}