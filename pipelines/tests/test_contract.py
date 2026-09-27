from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONF = yaml.safe_load((ROOT / "pipelines" / "conf" / "pipeline.yaml").read_text())


def test_required_keys():
    assert CONF["name"]
    assert CONF["source"]["tables"]
    assert CONF["destination"]["file_format"] == "parquet"
    assert CONF["destination"]["glue_database"]


def test_every_selected_table_has_columns():
    for table in CONF["source"]["tables"]:
        cols = CONF["tables"][table]["columns"]
        assert cols, table


def test_no_secrets_in_contract():
    raw = (ROOT / "pipelines" / "conf" / "pipeline.yaml").read_text().lower()
    for needle in ("password", "secret_access_key", "aws_secret", "token="):
        assert needle not in raw
