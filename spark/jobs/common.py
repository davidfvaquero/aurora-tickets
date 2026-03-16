import argparse
from pyspark.sql import SparkSession


def build_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .getOrCreate()
    )


def add_common_paths(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--student-id", required=True)
    parser.add_argument("--raw-clickstream", required=True)
    parser.add_argument("--raw-events", required=True)
    parser.add_argument("--raw-campaigns", required=True)
    parser.add_argument("--raw-transactions", required=True)
    parser.add_argument("--curated-base", required=True)
    parser.add_argument("--analytics-base", required=False)
    return parser
