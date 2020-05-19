terraform {
  required_version = "> 0.12.0"

  backend "s3" {
    bucket  = "project-terraform"
    key     = "bot-discogs"
    profile = "victor5114-automation"
    region  = "eu-west-3"
  }
}

provider "aws" {
  version = "~> 2.0"
  profile = "victor5114-automation"
  region  = "eu-west-3"
}

data "aws_availability_zones" "available" {}

data "aws_region" "current" {}

resource "aws_key_pair" "main" {
  key_name   = "kp-${local.project}"
  public_key = file("${path.root}/files/id_rsa.pub")
}

data "aws_caller_identity" "current" {}
