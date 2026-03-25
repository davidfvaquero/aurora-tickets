#!/usr/bin/env python3
import argparse
from pathlib import Path


def load_env(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def render_file(src: Path, dst: Path, replacements: dict[str, str]) -> None:
    text = src.read_text(encoding="utf-8")
    for needle, repl in replacements.items():
        text = text.replace(needle, repl)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Aurora cloud-init templates")
    parser.add_argument("--env-file", default="config/.env")
    parser.add_argument("--repo-archive-url", required=True)
    parser.add_argument("--spark-master-url", default="")
    parser.add_argument("--output-dir", default="build/cloud-init")
    args = parser.parse_args()

    env_values = load_env(Path(args.env_file))
    required = ["STUDENT_ID", "AWS_REGION"]
    missing = [key for key in required if key not in env_values]
    if missing:
      raise SystemExit(f"Missing keys in env file: {', '.join(missing)}")

    replacements = {
        "__REPO_ARCHIVE_URL__": args.repo_archive_url,
        "__STUDENT_ID__": env_values["STUDENT_ID"],
        "__AWS_REGION__": env_values["AWS_REGION"],
        "__SPARK_MASTER_URL__": args.spark_master_url,
    }

    template_dir = Path("infra/cloud-init")
    output_dir = Path(args.output_dir)
    for src in template_dir.glob("*.yaml"):
        render_file(src, output_dir / src.name, replacements)


if __name__ == "__main__":
    main()
