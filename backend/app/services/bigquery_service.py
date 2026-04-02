from google.cloud import bigquery
from datetime import datetime, timezone
import json
import uuid

PROJECT_ID = "rpa-doc-comparison"
DATASET_ID = "doc_comparison"
TABLE_ID = "comparison_results"

client = bigquery.Client(project=PROJECT_ID)


def insert_comparison_result(
    prior_auth_file: str,
    insurance_file: str,
    comparison_result: dict,
    prior_auth_fields: dict,
    insurance_fields: dict
):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    created_at = datetime.now(timezone.utc)
    created_at_iso = created_at.isoformat()

    row = {
        "comparison_id": str(uuid.uuid4()),
        "created_at": created_at_iso,
        "document_a": prior_auth_file,
        "document_b": insurance_file,
        "similarity_score": comparison_result["summary"].get("matched_count", 0),
        "matched_items": json.dumps(comparison_result.get("matched_fields", [])),
        "missing_items": json.dumps(comparison_result.get("missing_in_prior_auth", [])),
        "policy_fields": json.dumps(insurance_fields),
        "request_fields": json.dumps(prior_auth_fields),
        "field_comparison": json.dumps(comparison_result)
    }

    errors = client.insert_rows_json(table_ref, [row])

    if errors:
        raise Exception(f"BigQuery insert failed: {errors}")

    return row


def get_comparison_results():
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        ORDER BY created_at DESC
        LIMIT 20
    """

    results = client.query(query).result()

    rows = []
    for row in results:
        rows.append({
            "comparison_id": row.get("comparison_id"),
            "created_at": str(row.get("created_at")),
            "document_a": row.get("document_a"),
            "document_b": row.get("document_b"),
            "similarity_score": row.get("similarity_score"),
            "matched_items": row.get("matched_items"),
            "missing_items": row.get("missing_items"),
            "policy_fields": row.get("policy_fields"),
            "request_fields": row.get("request_fields"),
            "field_comparison": row.get("field_comparison"),
        })

    return rows