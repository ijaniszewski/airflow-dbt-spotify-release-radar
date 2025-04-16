FROM apache/airflow:2.10.5

# Switch to root to install system packages
USER root

# Install MySQL client libraries (for CLI or debugging, optional)
RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Add and install Python packages
ADD requirements.txt .

RUN pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt