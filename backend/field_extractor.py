import re


FIELD_PATTERNS = {
    "patient_name": [
        r"patient name\s*[:\-]\s*(.+)",
        r"name\s*[:\-]\s*(.+)"
    ],
    "date_of_birth": [
        r"date of birth\s*[:\-]\s*(.+)",
        r"dob\s*[:\-]\s*(.+)"
    ],
    "diagnosis": [
        r"diagnosis\s*[:\-]\s*(.+)"
    ],
    "icd_code": [
        r"icd[-\s]*code\s*[:\-]\s*(.+)",
        r"icd\s*[:\-]\s*(.+)"
    ],
    "medication_name": [
        r"drug\s*[:\-]\s*(.+)",
        r"medication\s*[:\-]\s*(.+)"
    ]
}


def clean_value(value: str) -> str:
    value = value.strip()
    value = value.split("\n")[0].strip()
    return value


def extract_fields(text: str) -> dict:
    extracted = {}
    lines = text.splitlines()

    for field, patterns in FIELD_PATTERNS.items():
        extracted[field] = None

        for line in lines:
            normalized_line = line.strip()

            for pattern in patterns:
                match = re.search(pattern, normalized_line, re.IGNORECASE)
                if match:
                    extracted[field] = clean_value(match.group(1))
                    break

            if extracted[field]:
                break

    return extracted