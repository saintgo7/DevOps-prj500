variable "region" {
  type        = string
  default     = "ap-northeast-2"
  description = "AWS region"
}

variable "azs" {
  type        = list(string)
  default     = ["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"]
  description = "Availability zones"
}
