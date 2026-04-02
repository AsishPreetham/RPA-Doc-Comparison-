from comparator import compare_texts


doc1 = """
Insurance approval is valid for 30 days.
Manual fax approval is accepted.
"""

doc2 = """
Insurance approval is valid for 15 days.
Pre-authorization is required for imaging.
"""

result = compare_texts(doc1, doc2)

print("\n=== RESULT ===\n")
print(result["llm_analysis"])