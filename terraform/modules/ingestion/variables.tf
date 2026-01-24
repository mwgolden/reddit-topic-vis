
variable "lambda_config" {
  type = map(object({
    function_name = string
    archive_src_path = string
    archive_build_path = string
    lambda_handler = string
    runtime = string
    environment_variables = map(any)
  }))
  description = "Configuration for lambda"

  validation {
    condition = alltrue([
      for k in keys(var.lambda_config) :
      contains(["comments", "more_comments"], k)
    ])
    error_message = "lambda_config keys must be one of: [comments, more_comments]"
  }
}

variable "download_s3_arn" {
  type = string
  description = "S3 arn for ingested data"
}

variable "api_token_cache_tables" {
  type = object({
    api_config_table = string,
    api_token_cache_table = string
  })
}