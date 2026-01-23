

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"
    actions = [ "sts:AssumeRole" ]
    principals {
      type = "service"
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
     resources = [ var.download_s3_path, "${var.download_s3_path}/*" ]
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

data "aws_iam_policy_document" "sqs_policy" {
  statement {
    effect = "Allow"
    principals {
      type = "*"
      identifiers = [ "*" ]
    }
    actions = [ "sqs:SendMessage" ]
    resources = aws_sqs_queue.reddit_more_comments_queue.arn
    condition {
      test = "ArnEquals"
      variable = "aws:SourceArn"
      values = [ aws_lambda_function.this["comments"].arn ]
    }
  }
}
