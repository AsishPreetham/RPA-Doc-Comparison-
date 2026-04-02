def build_comparison_prompt(diff_text: str) -> str:
    return f"""
You are an intelligent document comparison assistant.

Analyze the differences between two documents and provide structured output.

Your response MUST be in JSON format with the following fields:
- summary
- added_content
- removed_content
- modified_content (list of objects with old and new)
- risk_level (low, medium, high)
- recommendation

Here are the document differences:

{diff_text}

Return ONLY valid JSON.
"""