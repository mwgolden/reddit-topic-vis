
variable "account_id" {
  type = string
}

variable "region" {
  type = string
}

variable "data_bucket_name" {
  type = string
}

variable "lambda_config" {
  type = map(object({
    function_name = string
    archive_src_path = string
    archive_build_path = string
    lambda_handler = string
    runtime = string
    layers = list(string)
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

variable "event_source_config" {
  type = object({
    eventbridge_default_arn = string
    comment_load_event = object({
      name = string
      arn = string
    })
    post_load_event = object({
      name = string
      arn = string
    })
  })
}