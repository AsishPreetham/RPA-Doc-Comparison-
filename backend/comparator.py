def compare_structured_fields(prior_auth_fields: dict, insurance_fields: dict) -> dict:
    matched_fields = []
    mismatched_fields = []
    missing_in_prior_auth = []
    missing_in_insurance = []

    all_fields = set(prior_auth_fields.keys()).union(set(insurance_fields.keys()))

    for field in all_fields:
        prior_value = prior_auth_fields.get(field)
        insurance_value = insurance_fields.get(field)

        if prior_value and insurance_value:
            if prior_value.strip().lower() == insurance_value.strip().lower():
                matched_fields.append({
                    "field": field,
                    "prior_auth_value": prior_value,
                    "insurance_value": insurance_value
                })
            else:
                mismatched_fields.append({
                    "field": field,
                    "prior_auth_value": prior_value,
                    "insurance_value": insurance_value
                })

        elif insurance_value and not prior_value:
            missing_in_prior_auth.append({
                "field": field,
                "insurance_value": insurance_value
            })

        elif prior_value and not insurance_value:
            missing_in_insurance.append({
                "field": field,
                "prior_auth_value": prior_value
            })

    return {
        "matched_fields": matched_fields,
        "mismatched_fields": mismatched_fields,
        "missing_in_prior_auth": missing_in_prior_auth,
        "missing_in_insurance": missing_in_insurance,
        "summary": {
            "matched_count": len(matched_fields),
            "mismatched_count": len(mismatched_fields),
            "missing_in_prior_auth_count": len(missing_in_prior_auth),
            "missing_in_insurance_count": len(missing_in_insurance)
        }
    }