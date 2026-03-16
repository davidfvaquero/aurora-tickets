#!/usr/bin/env python3
import argparse

from pyspark.sql import functions as F

from common import build_spark


def parse_args():
    parser = argparse.ArgumentParser(description="Aurora Tickets Job 2: curated -> analytics + MySQL")
    parser.add_argument("--student-id", required=True)
    parser.add_argument("--curated-base", required=True)
    parser.add_argument("--analytics-base", required=True)
    parser.add_argument("--mysql-url", required=False)
    parser.add_argument("--mysql-user", required=False)
    parser.add_argument("--mysql-password", required=False)
    parser.add_argument("--mysql-driver", default="com.mysql.cj.jdbc.Driver")
    return parser.parse_args()


def load_curated(spark, curated_base):
    clickstream = spark.read.parquet(f"{curated_base}/clickstream")
    events = spark.read.parquet(f"{curated_base}/events")
    transactions = spark.read.parquet(f"{curated_base}/transactions")
    return clickstream, events, transactions


def build_funnel(clickstream):
    sessions = clickstream.select("dt", "session_id").dropDuplicates()
    totals = sessions.groupBy("dt").agg(F.count("*").alias("sessions_total"))

    def session_metric(event_name, alias):
        return (
            clickstream.filter(F.col("event_type") == event_name)
            .select("dt", "session_id")
            .dropDuplicates()
            .groupBy("dt")
            .agg(F.count("*").alias(alias))
        )

    funnel = totals
    for event_name, alias in [
        ("view_event_list", "sessions_event_list"),
        ("view_event_detail", "sessions_event_detail"),
        ("begin_checkout", "sessions_begin_checkout"),
        ("purchase", "sessions_purchase"),
    ]:
        funnel = funnel.join(session_metric(event_name, alias), on="dt", how="left")

    return (
        funnel.fillna(0)
        .withColumn(
            "conversion_rate",
            F.when(F.col("sessions_total") > 0, F.round(F.col("sessions_purchase") / F.col("sessions_total"), 4)).otherwise(F.lit(0.0)),
        )
        .orderBy("dt")
    )


def build_event_rank(clickstream, transactions):
    detail_views = (
        clickstream.filter(F.col("event_type") == "view_event_detail")
        .groupBy("dt", "event_id")
        .agg(F.count("*").alias("detail_views"))
    )
    purchases = (
        transactions.groupBy("dt", "event_id")
        .agg(
            F.count("*").alias("purchases"),
            F.round(F.sum("amount"), 2).alias("revenue_total"),
        )
    )

    return (
        detail_views.join(purchases, on=["dt", "event_id"], how="left")
        .fillna({"purchases": 0, "revenue_total": 0.0})
        .withColumn(
            "interest_to_purchase_ratio",
            F.when(F.col("purchases") > 0, F.round(F.col("detail_views") / F.col("purchases"), 4)).otherwise(None),
        )
        .orderBy("dt", F.desc("revenue_total"))
    )


def build_anomalies(clickstream, transactions):
    requests = (
        clickstream.groupBy("dt", "ip", "page")
        .agg(
            F.count("*").alias("requests"),
            F.sum(F.when(F.col("status_code") >= 400, 1).otherwise(0)).alias("errors"),
            F.sum(F.when(F.col("event_type") == "purchase", 1).otherwise(0)).alias("purchases"),
        )
    )

    purchases_by_session = transactions.groupBy("dt", "session_id").agg(F.count("*").alias("tx_count"))

    return (
        requests.join(clickstream.select("dt", "ip", "session_id").dropDuplicates(), on=["dt", "ip"], how="left")
        .join(purchases_by_session, on=["dt", "session_id"], how="left")
        .withColumn("tx_count", F.coalesce(F.col("tx_count"), F.lit(0)))
        .withColumn(
            "is_anomaly",
            (F.col("requests") >= 120)
            | (F.col("errors") >= 8)
            | ((F.col("requests") >= 80) & (F.col("tx_count") == 0)),
        )
        .withColumn(
            "reason",
            F.when(F.col("requests") >= 120, F.lit("high_request_volume"))
            .when(F.col("errors") >= 8, F.lit("high_error_volume"))
            .when((F.col("requests") >= 80) & (F.col("tx_count") == 0), F.lit("high_requests_without_transactions"))
            .otherwise(F.lit("normal")),
        )
        .select(
            "dt",
            F.lit("ip_page").alias("dimension"),
            "ip",
            "page",
            "requests",
            "errors",
            "purchases",
            "is_anomaly",
            "reason",
        )
    )


def write_table(df, target, partition_cols):
    df.write.mode("overwrite").partitionBy(*partition_cols).parquet(target)


def write_mysql(df, table_name, args):
    if not args.mysql_url:
        return
    (
        df.write.mode("overwrite")
        .format("jdbc")
        .option("url", args.mysql_url)
        .option("dbtable", table_name)
        .option("user", args.mysql_user)
        .option("password", args.mysql_password)
        .option("driver", args.mysql_driver)
        .save()
    )


def main():
    args = parse_args()
    spark = build_spark("aurora-analytics")
    clickstream, events, transactions = load_curated(spark, args.curated_base)

    funnel = build_funnel(clickstream)
    event_rank = build_event_rank(clickstream, transactions).join(events.select("event_id", "name"), on="event_id", how="left")
    anomalies = build_anomalies(clickstream, transactions)

    write_table(funnel, f"{args.analytics_base}/funnel_daily", ["dt"])
    write_table(event_rank, f"{args.analytics_base}/event_rank", ["dt"])
    write_table(anomalies, f"{args.analytics_base}/anomalies", ["dt", "dimension"])

    write_mysql(funnel, "metrics_funnel_daily", args)
    write_mysql(event_rank, "metrics_event_rank", args)
    write_mysql(anomalies, "metrics_anomalies", args)

    spark.stop()


if __name__ == "__main__":
    main()
