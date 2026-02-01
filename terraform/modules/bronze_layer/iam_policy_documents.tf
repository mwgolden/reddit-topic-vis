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


data "aws_iam_policy_document" "s3_read" {
  statement {
    effect = "Allow"
    actions = [
        "s3:ListBucket",
        "s3:GetObject"
     ]
     
     resources = [ "${data.aws_s3_bucket.reddit_bucket.arn}", "${data.aws_s3_bucket.reddit_bucket.arn}/raw/*", "${data.aws_s3_bucket.reddit_bucket.arn}/bronze/*" ]
  }
}

data "aws_iam_policy_document" "s3_write" {
  statement {
    effect = "Allow"
    actions = [ 
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"

     ]
     resources = [ "${data.aws_s3_bucket.reddit_bucket.arn}/bronze/*" ]
  }


}

data "aws_iam_policy_document" "glue_database" {
  statement {
    effect = "Allow"
    actions = [ 
        "glue:CreateDatabase"
     ]
     resources = [ "*" ]
  }
}

data "aws_iam_policy_document" "glue_catalog" {
  statement {
    effect = "Allow"
    actions = [ 
        "glue:GetDatabases",
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetTables",
     ]
     resources = [ "arn:aws:glue:${var.region}:${var.account_id}:catalog", "arn:aws:glue:${var.region}:${var.account_id}:database/${var.data_catalog.database_name}" ]
  }
}

data "aws_iam_policy_document" "glue_tables" {
  statement {
    effect = "Allow"
    actions = [ 
        "glue:GetTable",
        "glue:GetTables",
        "glue:CreateTable",
        "glue:UpdateTable",
        "glue:DeleteTable",
        "glue:GetTableVersion",
        "glue:GetTableVersions"
     ]
     resources = [ 
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}",
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/comments",
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/posts"
        ]
  }
}

data "aws_iam_policy_document" "glue_partitions" {
  statement {
    effect = "Allow"
    actions = [ 
        "glue:CreatePartition",
        "glue:BatchCreatePartition",
        "glue:GetPartition",
        "glue:GetPartitions",
        "glue:DeletePartition",
        "glue:BatchDeletePartition",
        "glue:UpdatePartition"
     ]
     resources = [ 
        "arn:aws:glue:${var.region}:${var.account_id}:database/${var.data_catalog.database_name}",
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/comments",
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/posts",
        "arn:aws:glue:${var.region}:${var.account_id}:catalog"
        ]
  }
}
