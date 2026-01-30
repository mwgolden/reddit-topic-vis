data "archive_file" "lambda" {
  for_each = var.lambda_config
  type = "zip"
  source_dir = each.value.archive_src_path
  output_path = each.value.archive_build_path
}


resource "aws_lambda_function" "this" {
  for_each = var.lambda_config

  function_name = each.value.function_name
  handler = each.value.lambda_handler
  runtime = each.value.runtime

  filename = data.archive_file.lambda[each.key].output_path
  source_code_hash = data.archive_file.lambda[each.key].output_base64sha256

  timeout = 60
  
  role = aws_iam_role.reddit_lambda_bronze_layer_role.arn
  
  environment {
    variables = each.value.environment_variables
  }
}