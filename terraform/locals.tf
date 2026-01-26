data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region = data.aws_region.current.region
  eventbridge_default_arn = "arn:aws:events:${local.region}:${local.account_id}:event-bus/default"
}