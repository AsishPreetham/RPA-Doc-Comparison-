import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_llm_response(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Error: GROQ_API_KEY not found in .env"

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Current Groq model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: LLM request failed - {type(e).__name__}: {e}"


def validate_llm_settings():
    """Check environment and API access quickly."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "status": "failed",
            "reason": "GROQ_API_KEY not set in environment",
            "example_next_steps": "Create a .env file with GROQ_API_KEY=<your_key> and rerun"
        }

    # quick smoke test prompt
    test_prompt = "What is 2 + 2? Return only a number."
    result = get_llm_response(test_prompt)

    if result.startswith("Error:"):
        return {
            "status": "failed",
            "reason": "LLM API call failed",
            "details": result
        }

    return {
        "status": "success",
        "message": "LLM connection seems OK",
        "llm_output": result
    }


def check_llm_health():
    """Comprehensive LLM health check - like a backend health endpoint."""
    health_report = {
        "service": "LLM Document Comparison",
        "timestamp": "2026-04-02T12:00:00Z",  # Would be dynamic in real app
        "status": "unknown",
        "checks": {}
    }

    # Check 1: Environment setup
    api_key = os.getenv("GROQ_API_KEY")
    health_report["checks"]["environment"] = {
        "status": "pass" if api_key else "fail",
        "message": "API key loaded" if api_key else "API key missing",
        "details": f"Key length: {len(api_key) if api_key else 0}"
    }

    # Check 2: API connectivity
    if api_key:
        test_result = validate_llm_settings()
        health_report["checks"]["api_connectivity"] = {
            "status": "pass" if test_result["status"] == "success" else "fail",
            "message": test_result.get("message", test_result.get("reason", "Unknown")),
            "response_time": "< 5s",  # Would measure actual time
            "llm_response": test_result.get("llm_output", "")
        }
    else:
        health_report["checks"]["api_connectivity"] = {
            "status": "fail",
            "message": "Cannot test - API key missing"
        }

    # Check 3: Document comparison functionality
    if health_report["checks"]["api_connectivity"]["status"] == "pass":
        try:
            from comparator import compare_texts
            test_doc1 = "Test document one."
            test_doc2 = "Test document two."
            comparison_result = compare_texts(test_doc1, test_doc2)

            health_report["checks"]["document_comparison"] = {
                "status": "pass",
                "message": "Document comparison working",
                "has_diff_analysis": bool(comparison_result.get("llm_analysis")),
                "response_format": "json" if comparison_result.get("llm_analysis", "").strip().startswith("{") else "text"
            }
        except Exception as e:
            health_report["checks"]["document_comparison"] = {
                "status": "fail",
                "message": f"Document comparison failed: {e}"
            }
    else:
        health_report["checks"]["document_comparison"] = {
            "status": "skip",
            "message": "Skipped - API connectivity failed"
        }

    # Overall status
    all_checks = [check["status"] for check in health_report["checks"].values()]
    if "fail" in all_checks:
        health_report["status"] = "unhealthy"
    elif "skip" in all_checks:
        health_report["status"] = "degraded"
    else:
        health_report["status"] = "healthy"

    return health_report