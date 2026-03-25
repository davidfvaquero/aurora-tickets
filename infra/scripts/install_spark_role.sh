#!/usr/bin/env bash
set -euo pipefail

ROLE="${1:?role required}"
SPARK_VERSION="${SPARK_VERSION:-3.5.1}"
HADOOP_VERSION="${HADOOP_VERSION:-3}"
INSTALL_DIR="/opt/spark"

sudo apt-get update -y
sudo apt-get install -y openjdk-11-jdk python3 python3-pip unzip curl

# Install AWS CLI v2 from the official zip because Ubuntu 24.04 images in Learner Lab
# may not provide a working awscli apt package.
if ! command -v aws >/dev/null 2>&1; then
  curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip
  rm -rf /tmp/aws
  unzip -oq /tmp/awscliv2.zip -d /tmp
  sudo /tmp/aws/install --update
fi

if [ ! -d "$INSTALL_DIR" ]; then
  curl -fsSL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" -o /tmp/spark.tgz
  sudo tar -xzf /tmp/spark.tgz -C /opt
  sudo ln -s "/opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" "$INSTALL_DIR"
fi

sudo mkdir -p /opt/aurora /etc/aurora
sudo chown -R ubuntu:ubuntu /opt/aurora /etc/aurora /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} "$INSTALL_DIR"

cat <<'EOF' | sudo tee /etc/profile.d/spark.sh >/dev/null
export SPARK_HOME=/opt/spark
export PATH=$PATH:/opt/spark/bin:/opt/spark/sbin
export PYSPARK_PYTHON=python3
EOF

case "$ROLE" in
  master)
    sudo cp infra/systemd/spark-master.service /etc/systemd/system/spark-master.service
    sudo systemctl daemon-reload
    sudo systemctl enable spark-master
    sudo systemctl restart spark-master
    ;;
  worker)
    sudo cp infra/systemd/spark-worker.service /etc/systemd/system/spark-worker.service
    sudo systemctl daemon-reload
    sudo systemctl enable spark-worker
    sudo systemctl restart spark-worker
    ;;
  submit)
    python3 -m pip install --break-system-packages pyspark boto3 mysql-connector-python
    ;;
  *)
    echo "Unsupported role: $ROLE" >&2
    exit 1
    ;;
esac
