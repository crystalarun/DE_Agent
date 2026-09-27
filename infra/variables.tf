variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "github_owner" {
  type        = string
  description = "GitHub user or org that owns the repo"
  default     = "crystalarun"
}

variable "github_repo" {
  type    = string
  default = "DE_Agent"
}

variable "budget_email" {
  type        = string
  description = "Email for the $5 AWS budget alarm"
}

variable "name_prefix" {
  type    = string
  default = "data-autopilot"
}
