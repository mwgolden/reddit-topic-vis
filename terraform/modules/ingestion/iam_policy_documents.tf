

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"
    actions = [ "sts:AssumeRole" ]
    principals {
      type = "Service"
      identifiers = [ "lambda.amazonaws.com" ]
    }
  }
}

data "aws_iam_policy_document" "lambda_logs_policy" {
  statement {
    effect = "Allow"
    actions = [ 
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
     ]
     resources = [ "arn:aws:logs:*:*:**" ]
  }
}

data "aws_iam_policy_document" "lambda_s3_policy" {
  statement {
    effect = "Allow"
    actions = [ 
        "s3:PutObject",
        "s3:GetObject",
        "s3:List*"
     ]
     resources = [ var.download_s3_arn, "${var.download_s3_arn}/*" ]
  }
}

data "aws_iam_policy_document" "publish_eventbridge_event" {
  statement {
    effect = "Allow"
    actions = [ 
      "events:PutEvents"
     ]
     resources = [ "*" ]
  }
}

data "aws_iam_policy_document" "sqs_producer_policy" {
  statement {
    effect = "Allow"
    actions = [ "sqs:SendMessage" ]
    resources = [aws_sqs_queue.reddit_more_comments_queue.arn]
  }
}

data "aws_iam_policy_document" "sqs_consumer_policy" {
  statement {
    effect = "Allow"
    actions = [ 
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ChangeMessageVisibility"
     ]
     resources = [ aws_sqs_queue.reddit_more_comments_queue.arn ]
  }
}

data "aws_iam_policy_document" "dynamodb_read_policy" {
  statement {
    effect = "Allow"
    actions = [ 
      "dynamodb:GetItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:DescribeTable"
     ]
     resources = [ data.aws_dynamodb_table.api_config_table.arn, data.aws_dynamodb_table.api_token_cache_table.arn ]
  }
}

data "aws_iam_policy_document" "dynamodb_insert_policy" {
  statement {
    effect = "Allow"
    actions = [ 
      "dynamodb:PutItem",
      "dynamodb:BatchWriteItem"
     ]
     resources = [ data.aws_dynamodb_table.api_token_cache_table.arn ]
  }
}
