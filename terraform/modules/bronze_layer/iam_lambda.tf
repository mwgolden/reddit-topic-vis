data "aws_iam_policy_document" "reddit_bronze_layer_policy" {
  source_policy_documents = [ 
    data.aws_iam_policy_document.lambda_logs_policy.json,
    data.aws_iam_policy_document.s3_read.json,
    data.aws_iam_policy_document.s3_write.json,
    data.aws_iam_policy_document.glue_catalog.json,
    data.aws_iam_policy_document.glue_database.json,
    data.aws_iam_policy_document.glue_tables.json,
    data.aws_iam_policy_document.glue_partitions.json
   ]
}

resource "aws_iam_policy" "reddit_lambda_bronze_layer_policy" {
  name = "reddit_bronze_layer_processing_policy"
  path = "/"
  description = "Policies for lambdas processing data for bronze layer"
  policy = data.aws_iam_policy_document.reddit_bronze_layer_policy.json
}

resource "aws_iam_role" "reddit_lambda_bronze_layer_role" {
  name = "reddit_bronze_layer_processing_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "attach_reddit_bronze_processing_policy" {
  role = aws_iam_role.reddit_lambda_bronze_layer_role.name
  policy_arn = aws_iam_policy.reddit_lambda_bronze_layer_policy.arn
}