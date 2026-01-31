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
     condition {
       test = "StringLike"
       variable = "s3:prefix"
       values = [ 
            "raw",
            "bronze"
        ]
     }
     resources = [ "${data.aws_s3_bucket.reddit_bucket.arn}", "${data.aws_s3_bucket.reddit_bucket.arn}/*" ]
  }
}

data "aws_iam_policy_document" "s3_write" {
  statement {
    effect = "Allow"
    actions = [ 
        "s3:PutObject",
        "s3:DeleteObject"
     ]
     condition {
       test = "StringLike"
       variable = "s3:prefix"
       values = [ 
            "bronze"
        ]
     }
     resources = [ "${data.aws_s3_bucket.reddit_bucket.arn}", "${data.aws_s3_bucket.reddit_bucket.arn}/*" ]
  }
}

data "aws_iam_policy_document" "glue_catalog" {
  statement {
    effect = "Allow"
    actions = [ 
        "glue:CreateDatabase",
        "glue:GetDatabases",
     ]
     resources = [ "arn:aws:glue:${var.region}:${var.account_id}:catalog"]
  }
}

data "aws_iam_policy_document" "glue_database" {
  statement {
    effect = "Allow"
    actions = [ 
        "glue:GetDatabase",
        "glue:GetSchema",
        "glue:GetSchemaVersion"
     ]
     resources = [ "arn:aws:glue:${var.region}:${var.account_id}:database/${var.data_catalog.database_name}"]
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
        "glue:DeleteTable"
     ]
     resources = [ 
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/${var.data_catalog.tables.posts_table}",
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/${var.data_catalog.tables.comments_table}"
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
        "glue:BatchDeletePartition"
     ]
     resources = [ 
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/${var.data_catalog.tables.posts_table}",
        "arn:aws:glue:${var.region}:${var.account_id}:table/${var.data_catalog.database_name}/${var.data_catalog.tables.comments_table}"
        ]
  }
}
