from difflib import ndiff
from prompts import build_comparison_prompt
from llm_service import get_llm_response


def compare_texts(text1: str, text2: str):
    diff = list(ndiff(text1.splitlines(), text2.splitlines()))

    added = []
    removed = []
    unchanged = []

    for line in diff:
        if line.startswith("+ "):
            added.append(line[2:])
        elif line.startswith("- "):
            removed.append(line[2:])
        elif line.startswith("  "):
            unchanged.append(line[2:])

    diff_text = "\n".join(diff)

    prompt = build_comparison_prompt(diff_text)

    llm_output = get_llm_response(prompt)

    return {
        "added": added,
        "removed": removed,
        "unchanged": unchanged,
        "llm_analysis": llm_output
    }