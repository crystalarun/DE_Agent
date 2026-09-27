#!/usr/bin/env python3
"""Extract configured SQL tables to S3 Parquet, then register Glue tables.

Secrets never belong in this file. AWS auth is the GitHub OIDC role.
A Postgres/MySQL source is provided via SOURCE_DATABASE_URL in GitHub Secrets.
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
            subprocess.check_call(
                [sys.executable, str(ROOT / "samples" / "build_chinook.py")]
            )
        return f"sqlite:///{db}"
    if kind == "sqlalchemy":
        url = os.environ.get("SOURCE_DATABASE_URL")
        if not url:
            raise SystemExit("SOURCE_DATABASE_URL is required for sqlalchemy sources")
        return url
    raise SystemExit(f"Unsupported source type: {kind}")


def resolve_tables(conf: dict, url: str) -> list[str]:
    src = conf["source"]
    tables = src.get("tables") or []
    # Empty list means "all tables in schema"
    if tables:
        return tables

    schema = src.get("schema")
    if not schema:
        raise SystemExit("source.schema is required when source.tables is empty")

    # Resolve table names at runtime (no secrets in contract).
    from sqlalchemy import create_engine, inspect

    engine = create_engine(url)
    try:
        insp = inspect(engine)
        names = insp.get_table_names(schema=schema)
    finally:
        engine.dispose()

    if not names:
        raise SystemExit(f"No tables found in schema '{schema}'")

    # Pass fully-qualified names for clarity.
    return [f"{schema}.{n}" for n in names]


def main() -> None:
    conf = load_conf()
    url = source_url(conf)
    tables = resolve_tables(conf, url)

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

    src_conf = conf["source"]
    schema = src_conf.get("schema")
    # If tables are schema-qualified, pass schema=None to avoid double-qualifying.
    src = sql_database(url, table_names=tables, schema=None if any("." in t for t in tables) else schema)

    info = pipeline.run(src, loader_file_format="parquet", write_disposition=write)
    print(info)

    from register_glue import register

    register(conf, bucket=bucket)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
