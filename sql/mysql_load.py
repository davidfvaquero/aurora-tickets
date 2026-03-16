#!/usr/bin/env python3
import argparse
import pathlib

import mysql.connector


def parse_args():
    parser = argparse.ArgumentParser(description="Apply Aurora MySQL schema")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--schema-file", default=str(pathlib.Path(__file__).with_name("schema.sql")))
    return parser.parse_args()


def main():
    args = parse_args()
    sql = pathlib.Path(args.schema_file).read_text(encoding="utf-8")
    conn = mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        allow_local_infile=True,
    )
    cur = conn.cursor()
    for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
        cur.execute(stmt)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
