import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
MENTOR_SLUG = os.getenv("MENTOR_SLUG")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_post_ai_mentor_metadata():
    endpoint_template = "/api/ai-mentor/orgs/{org}/metadata/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not MENTOR_SLUG:
        print("❌ Missing MENTOR_SLUG in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/metadata/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "metadata": {
            "test": "test"
        },
        "mentor": MENTOR_SLUG
    }

    print("🔍 Running Test: POST AI-Mentor Metadata")
    print(f"URL: {url}")
    print(f"Payload: {payload}")

    response = requests.post(url, headers=headers, json=payload)
    status_code = response.status_code

    if status_code in [200, 201]:
        print("✅ SUCCESS")

        try:
            data = response.json()
            summary = "Metadata created successfully"
        except ValueError:
            summary = "Metadata created (no response body)"

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "working",
            summary,
            "POST request succeeded and metadata was added"
        )
        return True

    elif status_code == 400:
        print("❌ 400 Bad Request")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "bad request",
            "Invalid payload provided",
            "Check required fields: metadata object and valid mentor slug"
        )
        return False

    elif status_code == 401:
        print("❌ 401 Unauthorized")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "auth failed",
            "Authentication failed",
            "Invalid or missing API token"
        )
        return False

    elif status_code == 403:
        print("❌ 403 Forbidden")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Access denied",
            "POST action appears restricted by role, tenant permissions, or environment configuration"
        )
        return False

    elif status_code == 404:
        print("❌ 404 Not Found")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "not found",
            "Endpoint not found",
            "Check org value or endpoint availability"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Unexpected response returned",
            "Manual review recommended"
        )
        return False


if __name__ == "__main__":
    test_post_ai_mentor_metadata()