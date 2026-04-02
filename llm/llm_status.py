#!/usr/bin/env python3
"""
Quick LLM Status Check - Like a ping endpoint
"""

from llm_service import validate_llm_settings
import json


def quick_llm_status():
    """Fast status check - returns simple pass/fail"""
    result = validate_llm_settings()

    status = {
        "llm_status": "up" if result["status"] == "success" else "down",
        "message": result.get("message", result.get("reason", "Unknown")),
        "timestamp": "2026-04-02T12:00:00Z"
    }

    return status


if __name__ == "__main__":
    status = quick_llm_status()
    print(json.dumps(status, indent=2))