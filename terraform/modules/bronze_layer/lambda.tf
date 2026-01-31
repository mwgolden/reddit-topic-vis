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

  timeout = 120
  memory_size = 2048
  
  role = aws_iam_role.reddit_lambda_bronze_layer_role.arn
  layers = [ "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:21" ]
  
  environment {
    variables = each.value.environment_variables
  }
}

resource "aws_cloudwatch_event_target" "this" {
  for_each = aws_lambda_function.this
  rule = var.event_source_config.events.name
  target_id = each.key
  arn = each.value.arn
}

resource "aws_lambda_permission" "eventbridge" {
  for_each = aws_lambda_function.this

  statement_id = "AllowEventBridgeInvoke-bronze-${each.key}"
  action = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal = "events.amazonaws.com"
  source_arn = var.event_source_config.events.arn
}