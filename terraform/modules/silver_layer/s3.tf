data "aws_s3_bucket" "reddit_bucket" {
  bucket = var.data_bucket_name
}