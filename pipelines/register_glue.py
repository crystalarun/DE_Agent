"""Register Parquet tables in Glue without running a crawler."""
from __future__ import annotations

import boto3
from botocore.exceptions import ClientError

TYPE_MAP = {
    "bigint": "bigint",
    "string": "string",
    "double": "double",
    "timestamp": "timestamp",
}


def register(conf: dict, bucket: str) -> None:
    region = conf["destination"]["aws_region"]
    database = conf["destination"]["glue_database"]
    dataset = conf["destination"]["dataset"]
    prefix = conf["destination"].get("s3_prefix", "lake")
    glue = boto3.client("glue", region_name=region)

    try:
        glue.create_database(DatabaseInput={"Name": database, "Description": "Data Autopilot lake"})
        print(f"Created Glue database {database}")
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "AlreadyExistsException":
            raise
        print(f"Glue database {database} already exists")

    for table in conf["source"]["tables"]:
        columns = [
            {"Name": name, "Type": TYPE_MAP[dtype]}
            for name, dtype in conf["tables"][table]["columns"].items()
        ]
        location = f"s3://{bucket}/{prefix}/{dataset}/{table.lower()}/"
        table_input = {
            "Name": f"{dataset}_{table.lower()}",
            "TableType": "EXTERNAL_TABLE",
            "Parameters": {"classification": "parquet", "EXTERNAL": "TRUE"},
            "StorageDescriptor": {
                "Columns": columns,
                "Location": location,
                "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
                },
            },
        }
        try:
            glue.create_table(DatabaseName=database, TableInput=table_input)
            print(f"Created Glue table {database}.{table_input['Name']} -> {location}")
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "AlreadyExistsException":
                raise
            glue.update_table(DatabaseName=database, TableInput=table_input)
            print(f"Updated Glue table {database}.{table_input['Name']} -> {location}")
