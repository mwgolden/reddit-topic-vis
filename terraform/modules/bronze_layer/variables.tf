
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
      contains(["comments", "posts"], k)
    ])
    error_message = "lambda_config keys must be one of: [comments, posts]"
  }
}

variable "account_id" {
  type = string
}

variable "region" {
  type = string
}

variable "data_bucket_name" {
  type = string
}

variable "eventbridge_default_arn" {
  type = string
}

variable "database_name" {
  type = string
}

variable "posts_table" {
  type = string
}

variable "comments_table" {
  type = string
}