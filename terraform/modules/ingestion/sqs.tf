resource "aws_sqs_queue" "reddit_more_comments_queue" {
  name = "reddit_more_comments_queue"
  max_message_size = 2048
  message_retention_seconds = 180
  visibility_timeout_seconds = 240
}

resource "aws_lambda_event_source_mapping" "reddit_more_comments_event_source_mapping" {
  event_source_arn = aws_sqs_queue.reddit_more_comments_queue.arn
  function_name = aws_lambda_function.this["more_comments"].arn
  batch_size = 2
}