terraform {
  required_version = ">= 1.9.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.70"
    }
  }
  # Backend example — fill in your bucket/key/region.
  # backend "s3" {
  #   bucket = "sdgi-tfstate-dev"
  #   key    = "envs/dev/terraform.tfstate"
  #   region = "ap-northeast-2"
  # }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      env     = "dev"
      project = "sdg-impact-cloud"
      owner   = "platform"
      managed = "terraform"
    }
  }
}

module "network" {
  source = "../../modules/network"

  name       = "sdgi-dev"
  cidr_block = "10.10.0.0/16"
  azs        = var.azs

  tags = {
    env = "dev"
  }
}
