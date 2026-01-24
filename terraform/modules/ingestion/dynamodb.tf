data "aws_dynamodb_table" "api_config_table" {
  name = var.api_token_cache_tables.api_config_table
}

data "aws_dynamodb_table" "api_token_cache_table" {
  name = var.api_token_cache_tables.api_token_cache_table
}