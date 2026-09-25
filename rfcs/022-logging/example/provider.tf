provider "aws" {
  region  = "eu-west-1"
  version = "~> 2.47.0"

  assume_role {
    role_arn = "arn:aws:iam::ACCOUNT_ID:role/platform-developer"
  }
}