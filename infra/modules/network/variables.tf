variable "name" {
  description = "Logical name prefix (e.g., sdgi-dev)"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.10.0.0/16"
}

variable "azs" {
  description = "Availability zones to deploy into"
  type        = list(string)
}

variable "tags" {
  description = "Common tags applied to every resource"
  type        = map(string)
  default     = {}
}
