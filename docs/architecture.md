# Architecture

```text
Agent answers (HTML form, Notion chat, or generate-pipeline workflow)
        |
        v
pipelines/conf/pipeline.yaml     # non-secret contract
        |
        v
GitHub Action ingest (OIDC, no AWS keys)
        |
        +--> dlt sql_database extract
        +--> Parquet objects in s3://$LAKE_BUCKET/lake/chinook/<table>/
        +--> Glue database `lake`, tables chinook_album, ...
        v
Athena / any Iceberg-later query engine
```

Airflow and Airbyte are out of scope for the free demo. GitHub Actions is the orchestrator. dlt is the extractor. S3 + Glue is the lake.
