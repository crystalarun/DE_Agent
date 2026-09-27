# AWS bootstrap (once)

You need the AWS CLI logged in as the free-account owner.

```bash
cd infra
terraform init
terraform apply -var='budget_email=YOUR_EMAIL@domain'
```

Copy outputs:

1. GitHub repository **secret** `AWS_ROLE_ARN` = `github_role_arn`
2. GitHub repository **variable** `LAKE_BUCKET` = `lake_bucket`
3. GitHub repository **variable** `AWS_REGION` = `us-east-1`

Do not create long-lived access keys.

Then: Actions → ingest → Run workflow.

Query in Athena:

```sql
SELECT ar.Name AS artist, COUNT(*) AS albums
FROM lake.chinook_album al
JOIN lake.chinook_artist ar ON al.ArtistId = ar.ArtistId
GROUP BY ar.Name
ORDER BY albums DESC;
```
