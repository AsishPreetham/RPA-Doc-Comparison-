#!/usr/bin/env python3
"""
LLM Health Check Script
Like a backend health endpoint for your LLM service
"""

import json
import sys
from llm_service import check_llm_health


def main():
    print("🔍 LLM Health Check")
    print("=" * 50)

    health = check_llm_health()

    # Overall status
    status_emoji = {
        "healthy": "✅",
        "degraded": "⚠️",
        "unhealthy": "❌"
    }

    print(f"Status: {status_emoji.get(health['status'], '❓')} {health['status'].upper()}")
    print(f"Service: {health['service']}")
    print()

    # Individual checks
    for check_name, check_data in health["checks"].items():
        check_emoji = {
            "pass": "✅",
            "fail": "❌",
            "skip": "⏭️"
        }

        print(f"{check_emoji.get(check_data['status'], '❓')} {check_name.replace('_', ' ').title()}")
        print(f"   {check_data['message']}")

        if check_data.get("details"):
            print(f"   Details: {check_data['details']}")

        if check_data.get("llm_response"):
            print(f"   LLM Response: {check_data['llm_response'][:50]}...")

        print()

    # Exit code based on health
    if health["status"] == "healthy":
        print("🎉 All systems operational!")
        sys.exit(0)
    elif health["status"] == "degraded":
        print("⚠️ Service is degraded but functional")
        sys.exit(1)
    else:
        print("❌ Service is unhealthy")
        sys.exit(2)


if __name__ == "__main__":
    main()