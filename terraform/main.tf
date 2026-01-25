
module "ingestion" {
  source = "./modules/ingestion"
  download_s3_arn = aws_s3_bucket.com_wgolden_reddit.arn
  api_token_cache_tables = var.api_token_cache_tables
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
            "API_ENDPOINT": "https://oauth.reddit.com/comments",
            "S3_BUCKET": aws_s3_bucket.com_wgolden_reddit.id
        }
    }
  }
}