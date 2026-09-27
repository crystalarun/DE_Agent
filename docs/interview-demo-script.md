# 5-minute interview script

1. Problem: JDBC/SQL → lake is boilerplate. This repo automates the boilerplate, not judgment.
2. Open `agent/index.html` or GitHub Actions `generate-pipeline`. Show the contract, not a prompt dump.
3. Open `infra/main.tf` and `.github/workflows/ingest.yml`. Point at OIDC. No access keys.
4. Run ingest. Show Parquet in S3 and Glue tables.
5. Athena join on artist/album.
6. Cost: $5 budget, 30-day expiry, no MWAA.
7. What a company would add: VPC source, true JDBC via Glue, Iceberg, data contracts, PII.

Backup: keep a screenshot of a green ingest run.
