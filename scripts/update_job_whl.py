from databricks.sdk import WorkspaceClient
import os

# Read environment variables
host = os.environ["DATABRICKS_HOST"]
token = os.environ["DATABRICKS_TOKEN"]
whl_version = os.environ["WHL_VERSION"]
job_id = os.environ["JOB_ID"]

# Initialize Databricks client
w = WorkspaceClient(host=host, token=token)

# Wheel path (adjust to your storage location)
whl_path = f"dbfs:/FileStore/wheels/my_package-{whl_version}-py3-none-any.whl"

# Fetch job settings
job = w.jobs.get(job_id=job_id)
tasks = job.settings.tasks

# Update libraries for each task
for task in tasks:
    task.libraries = [{"whl": whl_path}]

# Reset job with updated settings
w.jobs.reset(
    job_id=job_id,
    new_settings=job.settings
)

print(f"Job {job_id} updated with wheel {whl_path}")
