data "aws_iam_policy_document" "reddit_download_comments_policy_combined" {
  source_policy_documents = [ 
    data.aws_iam_policy_document.lambda_logs_policy,
    data.aws_iam_policy_document.lambda_s3_policy,
    data.aws_iam_policy_document.publish_eventbridge_event
   ]
}

resource "aws_iam_policy" "reddit_download_comments_policy" {
  name = "reddit_download_comments_policy"
  path = "/"
  description = "AWS IAM policy for reddit download comments lambda"
  policy = data.aws_iam_policy_document.reddit_download_comments_policy_combined.json
}

resource "aws_iam_role" "reddit_download_comments_role" {
  name = "reddit_download_comments_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "attach_reddit_download_comments_policy" {
  role = aws_iam_role.reddit_download_comments_role.name
  policy_arn = data.aws_iam_policy_document.reddit_download_comments_policy_combined.arn
}