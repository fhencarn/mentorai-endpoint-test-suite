import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
MENTOR_SLUG = os.getenv("MENTOR_SLUG")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_mentor_settings():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentors/{mentor}/settings/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not MENTOR_SLUG:
        print("❌ Missing MENTOR_SLUG in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentors/{MENTOR_SLUG}/settings/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: GET Mentor Settings (Admin)")
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    status_code = response.status_code

    if status_code == 200:
        print("✅ SUCCESS (No Body Expected)")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "working",
            "Mentor settings endpoint accessible (no response body)",
            "Validated admin-only endpoint; response intentionally empty"
        )
        return True

    elif status_code == 401:
        print("❌ 401 Unauthorized")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
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
            "GET",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Access denied (admin-only endpoint)",
            "User likely not tenant admin"
        )
        return False

    elif status_code == 404:
        print("❌ 404 Not Found")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "not found",
            "Mentor settings not found",
            "Check mentor slug or user_id"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Unexpected response returned",
            "Manual review recommended"
        )
        return False


if __name__ == "__main__":
    test_get_mentor_settings()