#!/usr/bin/env python3
"""Apply non-secret answers onto pipelines/conf/pipeline.yaml."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONF_PATH = ROOT / "pipelines" / "conf" / "pipeline.yaml"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--answers", type=Path)
    parser.add_argument("--source-type")
    parser.add_argument("--tables")
    parser.add_argument("--write-disposition", default="replace")
    parser.add_argument("--schedule", default="manual")
    parser.add_argument("--aws-region", default="us-east-1")
    args = parser.parse_args()

    answers = json.loads(args.answers.read_text()) if args.answers else {}
    answers.setdefault("source_type", args.source_type or "chinook_sqlite")
    if "tables" not in answers:
        answers["tables"] = [
            t.strip()
            for t in (args.tables or "Album,Artist,Track,Invoice").split(",")
            if t.strip()
        ]
    answers.setdefault("write_disposition", args.write_disposition)
    answers.setdefault("schedule", args.schedule)
    answers.setdefault("aws_region", args.aws_region)

    conf = yaml.safe_load(CONF_PATH.read_text())
    conf["source"]["type"] = answers["source_type"]
    conf["source"]["tables"] = answers["tables"]
    conf["source"]["write_disposition"] = answers["write_disposition"]
    conf["schedule"] = answers["schedule"]
    conf["destination"]["aws_region"] = answers["aws_region"]
    CONF_PATH.write_text(yaml.safe_dump(conf, sort_keys=False))
    print(f"Updated {CONF_PATH}")
    print(json.dumps(answers, indent=2))


if __name__ == "__main__":
    main()
