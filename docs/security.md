# Security

- Never commit AWS keys, database passwords, or GitHub PATs.
- GitHub authenticates to AWS with OIDC. The IAM role trust is locked to `repo:crystalarun/DE_Agent:*`.
- Database URLs for a future live source go in GitHub Secret `SOURCE_DATABASE_URL`.
- S3 Block Public Access is on. Objects expire after 30 days.
- This HTML agent and Notion must never collect secrets.
