# Cost

Stay in us-east-1. Do not create EC2, RDS, NAT, MWAA, Glue crawlers, or Glue Spark jobs.

Expected demo cost: cents to low dollars.

| Thing | Why it is cheap |
| --- | --- |
| GitHub Actions public repo | Free minutes |
| Glue Data Catalog | First 1M objects/requests free |
| S3 Parquet | Tiny Chinook footprint + 30-day expiry |
| Athena | Query with LIMIT; ~$5/TB scanned |
| AWS Budget | Alarms at $1 (20% of $5) and $4 |

Destroy the stack with `terraform destroy` after the interview if you want the bill at zero.
