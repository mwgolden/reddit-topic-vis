resource "aws_s3_bucket" "com_wgolden_publish" {
  bucket = var.publish_bucket_name
}