# Deployment

## Reproducibility strategy

The repository uses versioned scripts and cloud-init assets instead of manual SSH installation. This satisfies the assignment rule that deployment must be automated.

## End-to-end flow

1. Provision the 6 EC2 instances with the provided cloud-init files.
2. Generate business CSVs and the frontend `events.json`.
3. Send data to the web node through a combination of replay and real HTTP traffic.
4. Upload raw files to S3.
5. Run Spark Job 1 and then Spark Job 2 from the submit node.
6. Validate CloudWatch, S3, Spark UI, and RDS evidence.

## Cost estimate

Document AWS Learner Lab pricing assumptions in the final PDF and include screenshots from the AWS calculator or a simple approximation by service and running hours.
