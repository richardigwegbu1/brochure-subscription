variable "aws_region" {
  default = "us-east-1"
}

variable "ami_id" {
  description = "RHEL 9 ID"
  default     = "ami-0c15e602d3d6c6c4a" # RHEL 9 in us-east-1
}

variable "instance_type" {
  default = "t3.micro"
}

variable "public_key_path" {
  description = "Path to SSH public key"
}

variable "private_key_path" {
  description = "Path to SSH private key"
}

variable "s3_bucket_name" {
  description = "S3 bucket name"
}

