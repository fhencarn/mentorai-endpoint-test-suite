import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_KEY")


# ========================
# MATRIX OUTPUT HELPERS
# ========================
def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


# ========================
# TEST FUNCTION
# ========================
def test_create_mentor_wizard():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/create-mentor-wizard/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/create-mentor-wizard/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": "Endpoint Wizard Test Mentor",
        "description": "This is a test mentor created by the create mentor wizard endpoint for endpoint validation."
    }

    print("🔍 Running Test: POST Create Mentor Wizard")
    print(f"URL: {url}")
    print(f"Payload: {payload}")

    response = requests.post(url, headers=headers, json=payload)
    status_code = response.status_code

    try:
        data = response.json()
    except Exception:
        print("❌ Response is not JSON")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "error",
            "Non-JSON response returned",
            "Failed to parse response"
        )
        return False

    # ========================
    # SUCCESS CASE
    # ========================
    if status_code == 200 or status_code == 201:
        name = data.get("name")
        unique_id = data.get("unique_id")
        slug = data.get("slug")

        response_summary = f"Mentor wizard created mentor '{name}'"
        notes = f"Returned unique_id={unique_id}, slug={slug}"

        print("✅ SUCCESS")
        print(f"Mentor Name: {name}")
        print(f"Unique ID: {unique_id}")
        print(f"Slug: {slug}")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "working",
            response_summary,
            notes
        )
        return True

    # ========================
    # ERROR CASES
    # ========================
    elif status_code == 400:
        print("❌ 400 Bad Request")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "bad request",
            "Invalid name or description payload",
            "Check required fields and description length"
        )
        return False

    elif status_code == 401:
        print("❌ 401 Unauthorized")
        print(data)

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
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Access denied",
            "Likely RBAC restriction"
        )
        return False

    elif status_code == 404:
        print("❌ 404 Not Found")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "not found",
            "Endpoint or resource not found",
            "Check org, user_id, or endpoint path"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Unexpected response",
            "Manual review required"
        )
        return False


# ========================
# RUN TEST
# ========================
if __name__ == "__main__":
    test_create_mentor_wizard()