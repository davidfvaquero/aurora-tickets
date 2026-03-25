# Cloud-Init Assets

These files implement the automated provisioning option required by the assignment.

- `web-node.yaml`: installs Nginx, FastAPI backend, static frontend, and CloudWatch Agent.
- `spark-master.yaml`: provisions the master node.
- `spark-worker-1.yaml`, `spark-worker-2.yaml`, `spark-worker-3.yaml`: provision the three workers.
- `spark-submit.yaml`: provisions the submit node and helper environment.

Before launching EC2 instances, replace these placeholders:

- `__REPO_ARCHIVE_URL__`
- `__STUDENT_ID__`
- `__AWS_REGION__`
- `__SPARK_MASTER_URL__`

To avoid editing YAML files by hand, render ready-to-paste user-data files with:

```bash
python3 infra/scripts/render_cloud_init.py \
  --env-file config/.env \
  --repo-archive-url "<presigned_or_public_zip_url>"
```

After the master is created and you know its private DNS or IP, render again for workers and submit:

```bash
python3 infra/scripts/render_cloud_init.py \
  --env-file config/.env \
  --repo-archive-url "<presigned_or_public_zip_url>" \
  --spark-master-url "spark://<master-private-ip>:7077"
```

Rendered files are written to `build/cloud-init/`.
