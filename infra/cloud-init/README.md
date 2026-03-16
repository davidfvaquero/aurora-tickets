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
