resource "aws_s3_bucket" "com_wgolden_reddit" {
  bucket = var.data_bucket_name
}

data "aws_iam_policy_document" "athena_bucket_policy" {
  statement {
    sid    = "AllowAthenaBucketMetadata"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["athena.amazonaws.com"]
    }

    actions = [
      "s3:GetBucketLocation",
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.com_wgolden_reddit.arn
    ]
  }

  statement {
    sid    = "AllowAthenaObjectWrites"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["athena.amazonaws.com"]
    }

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:AbortMultipartUpload",
      "s3:ListMultipartUploadParts"
    ]

    resources = [
      "${aws_s3_bucket.com_wgolden_reddit.arn}/*"
    ]
  }
}

resource "aws_s3_bucket_policy" "com_wgolden_reddit_policy" {
  bucket = aws_s3_bucket.com_wgolden_reddit.id
  policy = data.aws_iam_policy_document.athena_bucket_policy.json
}

