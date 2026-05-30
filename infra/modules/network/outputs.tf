output "vpc_id" {
  value       = aws_vpc.this.id
  description = "VPC ID"
}

output "public_subnet_ids" {
  value       = aws_subnet.public[*].id
  description = "Public subnet IDs"
}

output "private_app_subnet_ids" {
  value       = aws_subnet.private_app[*].id
  description = "Private app subnet IDs"
}

output "private_data_subnet_ids" {
  value       = aws_subnet.private_data[*].id
  description = "Private data subnet IDs"
}
