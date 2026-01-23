terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
  backend "s3" {
    bucket = "com.wgolden.tfstate"
    key    = "reddit-comments-visualization/tfstate"
    region = "us-east-1"
  }
}