resource "aws_sqs_queue" "reddit_more_comments_queue" {
  name = "reddit_more_comments_queue"
  max_message_size = 2048
  message_retention_seconds = 180
  visibility_timeout_seconds = 240
}

resource "aws_sqs_queue_policy" "reddit_more_commenrs_queue_policy" {
  queue_url = aws_sqs_queue.reddit_more_comments_queue.id
  policy = data.aws_iam_policy_document.sqs_policy.json
}

