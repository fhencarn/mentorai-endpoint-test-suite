import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
MENTOR_ID = os.getenv("MENTOR_ID")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_post_ai_mentor_sessions():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/sessions/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not MENTOR_ID:
        print("❌ Missing MENTOR_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/sessions/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "mentor": MENTOR_ID
    }

    print("🔍 Running Test: POST AI-Mentor Sessions")
    print(f"URL: {url}")
    print(f"Payload: {payload}")

    response = requests.post(url, headers=headers, json=payload)
    status_code = response.status_code

    if status_code == 200:
        print("✅ SUCCESS")

        try:
            data = response.json()
            session_id = data.get("session_id", "unknown")
            summary = f"Session created successfully (session_id: {session_id})"
        except ValueError:
            summary = "Session created but response was not valid JSON"

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "working",
            summary,
            "Successfully created mentor session and returned session_id"
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
            "Invalid payload",
            "Check mentor field and confirm this endpoint requires /users/{user_id}/sessions/"
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
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "not found",
            "Mentor or endpoint not found",
            "Check mentor slug, user_id, or endpoint path"
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
    test_post_ai_mentor_sessions()