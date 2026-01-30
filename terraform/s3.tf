resource "aws_s3_bucket" "com_wgolden_reddit" {
  bucket = var.data_bucket_name
}