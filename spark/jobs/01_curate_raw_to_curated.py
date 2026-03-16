#!/usr/bin/env python3
import argparse

from pyspark.sql import functions as F
from pyspark.sql import types as T

from common import add_common_paths, build_spark


def parse_args():
    parser = argparse.ArgumentParser(description="Aurora Tickets Job 1: raw -> curated")
    add_common_paths(parser)
    return parser.parse_args()


def curate_clickstream(spark, args):
    raw = spark.read.json(args.raw_clickstream)

    curated = (
        raw.withColumn("timestamp_ts", F.to_timestamp("timestamp"))
        .withColumn("dt", F.coalesce(F.col("dt"), F.to_date("timestamp_ts").cast("string")))
        .withColumn("event_id", F.col("event_id").cast("int"))
        .withColumn("amount", F.col("amount").cast("double"))
        .withColumn("status_code", F.col("status_code").cast("int"))
        .withColumn("latency_ms", F.col("latency_ms").cast("double"))
        .withColumn("source", F.coalesce("source", F.lit("unknown")))
        .withColumn("event_type", F.coalesce("event_type", F.lit("unknown")))
        .withColumn("page", F.coalesce("page", F.lit("/unknown")))
        .withColumn("utm_campaign", F.when(F.trim(F.col("utm_campaign")) == "", None).otherwise(F.col("utm_campaign")))
        .filter(F.col("student_id") == args.student_id)
        .filter(F.col("timestamp_ts").isNotNull())
        .filter(F.col("dt").isNotNull())
    )

    curated.write.mode("overwrite").partitionBy("dt", "source").parquet(f"{args.curated_base}/clickstream")


def curate_events(spark, args):
    schema = T.StructType(
        [
            T.StructField("event_id", T.StringType()),
            T.StructField("name", T.StringType()),
            T.StructField("city", T.StringType()),
            T.StructField("category", T.StringType()),
            T.StructField("event_date", T.StringType()),
            T.StructField("base_price", T.StringType()),
            T.StructField("capacity", T.StringType()),
            T.StructField("is_active", T.StringType()),
            T.StructField("description", T.StringType()),
            T.StructField("created_at", T.StringType()),
        ]
    )
    raw = spark.read.option("header", True).schema(schema).csv(args.raw_events)
    curated = (
        raw.withColumn("event_id", F.col("event_id").cast("int"))
        .withColumn("base_price_num", F.col("base_price").cast("double"))
        .withColumn("capacity_num", F.col("capacity").cast("int"))
        .withColumn("event_date_date", F.to_date("event_date"))
        .withColumn("is_active_int", F.col("is_active").cast("int"))
        .filter(F.col("event_id").isNotNull())
        .filter(F.col("name").isNotNull() & (F.trim("name") != ""))
        .filter(F.col("city").isNotNull() & (F.trim("city") != ""))
        .filter(F.col("category").isNotNull() & (F.trim("category") != ""))
        .filter(F.col("base_price_num").between(5, 500))
        .filter(F.col("capacity_num").between(50, 100000))
        .filter(F.col("event_date_date").isNotNull())
        .select(
            "event_id",
            "name",
            "city",
            "category",
            F.col("event_date_date").alias("event_date"),
            F.col("base_price_num").alias("base_price"),
            F.col("capacity_num").alias("capacity"),
            F.col("is_active_int").alias("is_active"),
            "description",
            "created_at",
        )
        .dropDuplicates(["event_id"])
    )
    curated.write.mode("overwrite").partitionBy("category").parquet(f"{args.curated_base}/events")


def curate_campaigns(spark, args):
    raw = spark.read.option("header", True).csv(args.raw_campaigns)
    curated = (
        raw.withColumn("monthly_cost_num", F.col("monthly_cost").cast("double"))
        .withColumn("start_dt_date", F.to_date("start_dt"))
        .withColumn("end_dt_date", F.to_date("end_dt"))
        .filter(F.col("utm_campaign").isNotNull() & (F.trim("utm_campaign") != ""))
        .filter(F.col("channel").isNotNull() & (F.trim("channel") != ""))
        .filter(F.col("monthly_cost_num").between(0, 100000))
        .select(
            "campaign_id",
            "utm_campaign",
            "channel",
            F.col("monthly_cost_num").alias("monthly_cost"),
            F.col("start_dt_date").alias("start_dt"),
            F.col("end_dt_date").alias("end_dt"),
            "created_at",
        )
        .dropDuplicates(["utm_campaign"])
    )
    curated.write.mode("overwrite").partitionBy("channel").parquet(f"{args.curated_base}/campaigns")


def curate_transactions(spark, args):
    raw = spark.read.option("header", True).csv(args.raw_transactions)
    curated = (
        raw.withColumn("timestamp_ts", F.to_timestamp("timestamp"))
        .withColumn("dt", F.coalesce(F.col("dt"), F.to_date("timestamp_ts").cast("string")))
        .withColumn("event_id", F.col("event_id").cast("int"))
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("amount_num", F.col("amount").cast("double"))
        .filter(F.col("transaction_id").isNotNull() & (F.trim("transaction_id") != ""))
        .filter(F.col("timestamp_ts").isNotNull())
        .filter(F.col("event_id").isNotNull())
        .filter(F.col("quantity").between(1, 10))
        .filter(F.col("amount_num").between(1, 5000))
        .select(
            "transaction_id",
            "timestamp_ts",
            "dt",
            "session_id",
            "event_id",
            "quantity",
            F.col("amount_num").alias("amount"),
            "payment_method",
            "utm_campaign",
            "created_at",
        )
        .dropDuplicates(["transaction_id"])
    )
    curated.write.mode("overwrite").partitionBy("dt", "payment_method").parquet(f"{args.curated_base}/transactions")


def main():
    args = parse_args()
    spark = build_spark("aurora-curation")
    curate_clickstream(spark, args)
    curate_events(spark, args)
    curate_campaigns(spark, args)
    curate_transactions(spark, args)
    spark.stop()


if __name__ == "__main__":
    main()
