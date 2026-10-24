
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_requesting_account_id  = true 
  access_key                  = "test"
  secret_key                  = "test"
  s3_use_path_style           = true

  endpoints {
    s3        = "http://localhost:4566"
    dynamodb  = "http://localhost:4566"
    sns       = "http://localhost:4566"
    sqs       = "http://localhost:4566"
    iam       = "http://localhost:4566"
    lambda    = "http://localhost:4566"
    apigateway = "http://localhost:4566"
  }
}
