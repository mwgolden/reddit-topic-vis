locals {
    lambda_roles = {
     comments = aws_iam_role.reddit_download_comments_role.arn
    }
}