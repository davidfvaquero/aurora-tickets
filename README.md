# Aurora Tickets

Submission-ready project scaffold for the Aurora Tickets Big Data assignment. The repository is built around the provided `Tema 4` starter assets and extends them with the missing pieces required by the PDF: Spark jobs, AWS provisioning assets for the 6-node topology, CloudWatch queries/dashboard templates, MySQL schema, CRISP-DM documentation, and evidence structure.

## Repository layout

- `webapp/`: static frontend, FastAPI backend, deployment scripts for the web node.
- `generators/`: business CSV generator with intentional data quality issues.
- `simulators/`: clickstream replay plus real HTTP traffic driver.
- `spark/`: Job 1 for curation and Job 2 for analytics plus MySQL load.
- `infra/`: cloud-init assets, systemd units, and Spark installation scripts.
- `cloudwatch/`: CloudWatch Agent template, saved query files, dashboard template.
- `sql/`: MySQL schema and helper loader.
- `docs/`: CRISP-DM markdown files.
- `evidence/`: screenshot checklist for the final delivery.

## Mandatory architecture covered

- EC2-1 Spark Master
- EC2-2 Spark Worker 1
- EC2-3 Spark Worker 2
- EC2-4 Spark Worker 3
- EC2-5 Spark Submit node
- EC2-6 Web + FastAPI + CloudWatch Agent

## Quick start

1. Set your identifiers in `config/project.env.example` and `webapp/frontend/js/config.js`.
2. Generate business data:

```bash
python generators/generate_business_data.py \
  --student-id <student_id> \
  --days 7 \
  --n-events 120 \
  --n-campaigns 12 \
  --n-transactions 20000 \
  --out-dir ./output_business \
  --frontend-data-dir ./webapp/frontend/data
```

3. Deploy the web node with `webapp/deploy/install_web_stack.sh` or the matching cloud-init file.
4. Generate clickstream with a mix of:

```bash
python simulators/replay_clickstream.py \
  --student-id <student_id> \
  --days 7 \
  --n-events 200000 \
  --events-json ./webapp/frontend/data/events.json \
  --campaigns-csv ./output_business/campaigns.csv \
  --out /var/log/aurora/aurora_clickstream.jsonl \
  --append
```

```bash
python simulators/traffic_driver.py \
  --base-url http://<web-public-ip> \
  --student-id <student_id> \
  --events-json ./webapp/frontend/data/events.json \
  --campaigns-csv ./output_business/campaigns.csv \
  --sessions 300
```

5. Upload raw data to S3 under `aurora/<student_id>/raw/`.
6. Run Spark Job 1, then Spark Job 2, from the submit node using `spark/README.md`.
7. Apply `sql/schema.sql` and verify the final MySQL tables.
8. Import the CloudWatch query files and `cloudwatch/dashboard-template.json`.

## Deliverable alignment

- 4 saved Logs Insights queries: included in `cloudwatch/queries/`
- 1 CloudWatch dashboard template: included
- 2 Spark jobs: included
- 3 final MySQL metrics tables: included
- CRISP-DM documentation structure: included
- Evidence folder: included

## Remaining manual work

You still need to replace placeholders such as `__STUDENT_ID__`, configure actual AWS resource names, run the deployment in AWS Learner Lab, and capture the evidence required for the final submission.
