from google.cloud import bigquery

client = bigquery.Client(project="your-actual-project-id")
query = "SELECT 1 AS test_value"
rows = client.query(query).result()

for row in rows:
    print(row["test_value"])