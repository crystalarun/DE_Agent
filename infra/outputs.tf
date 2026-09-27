output "lake_bucket" {
  value = aws_s3_bucket.lake.bucket
}

output "glue_database" {
  value = aws_glue_catalog_database.lake.name
}

output "github_role_arn" {
  value = aws_iam_role.github_ingest.arn
}

output "next_github_secrets" {
  value = {
    AWS_ROLE_ARN = aws_iam_role.github_ingest.arn
  }
}

output "next_github_variables" {
  value = {
    LAKE_BUCKET = aws_s3_bucket.lake.bucket
    AWS_REGION  = var.aws_region
  }
}
