#!/usr/bin/env python3
"""Extract configured SQL tables to S3 Parquet, then register Glue tables.

Secrets never belong in this file. AWS auth is the GitHub OIDC role.
A future Postgres/MySQL source is SOURCE_DATABASE_URL in GitHub Secrets.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import dlt
import yaml
from dlt.sources.sql_database import sql_database

ROOT = Path(__file__).resolve().parents[1]
CONF_PATH = ROOT / "pipelines" / "conf" / "pipeline.yaml"


def load_conf() -> dict:
    with CONF_PATH.open() as fh:
        return yaml.safe_load(fh)


def source_url(conf: dict) -> str:
    src = conf["source"]
    kind = src["type"]
    if kind == "chinook_sqlite":
        db = ROOT / "samples" / "chinook.sqlite"
        if not db.exists():
            subprocess.check_call([sys.executable, str(ROOT / "samples" / "build_chinook.py")])
        return f"sqlite:///{db}"
    if kind == "sqlalchemy":
        url = os.environ.get("SOURCE_DATABASE_URL")
        if not url:
            raise SystemExit("SOURCE_DATABASE_URL is required for sqlalchemy sources")
        return url
    raise SystemExit(f"Unsupported source type: {kind}")


def main() -> None:
    conf = load_conf()
    tables = conf["source"]["tables"]
    write = conf["source"].get("write_disposition", "replace")
    dataset = conf["destination"]["dataset"]
    bucket = os.environ.get("LAKE_BUCKET")
    prefix = conf["destination"].get("s3_prefix", "lake")
    if not bucket:
        raise SystemExit("LAKE_BUCKET env var is required, e.g. my-data-autopilot-bucket")

    os.environ.setdefault(
        "DESTINATION__FILESYSTEM__BUCKET_URL", f"s3://{bucket}/{prefix}"
    )

    pipeline = dlt.pipeline(
        pipeline_name=conf["name"],
        destination="filesystem",
        dataset_name=dataset,
        progress="log",
    )
    src = sql_database(source_url(conf), table_names=tables)
    info = pipeline.run(src, loader_file_format="parquet", write_disposition=write)
    print(info)

    from register_glue import register

    register(conf, bucket=bucket)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
