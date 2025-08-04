terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }
}


provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Environment = upper("${var.environment}")
    }
  }
}
