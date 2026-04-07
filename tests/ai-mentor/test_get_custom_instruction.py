import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_custom_instruction():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/custom-instruction/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/custom-instruction/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: GET Custom Instruction")
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    status_code = response.status_code

    try:
        data = response.json()
    except Exception:
        print("❌ Response is not JSON")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "error",
            "Non-JSON response returned",
            "Failed to parse response body"
        )
        return False

    if status_code == 200:
        instruction_id = data.get("id")
        about_user = data.get("about_user")
        mentor_tone = data.get("mentor_tone")

        about_user_status = "present" if about_user not in [None, ""] else "empty"
        mentor_tone_status = "present" if mentor_tone not in [None, ""] else "empty"

        response_summary = (
            f"Custom instruction retrieved: id={instruction_id}, "
            f"about_user={about_user_status}, mentor_tone={mentor_tone_status}"
        )
        notes = "Validated custom instruction endpoint and returned expected object fields (id, about_user, mentor_tone)"

        print("✅ SUCCESS")
        print(f"ID: {instruction_id}")
        print(f"About User: {about_user}")
        print(f"Mentor Tone: {mentor_tone}")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "working",
            response_summary,
            notes
        )
        return True

    elif status_code == 401:
        print("❌ 401 Unauthorized")
        print(data)

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
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Request authenticated but access denied",
            "Likely RBAC or org/user permission restriction"
        )
        return False

    elif status_code == 404:
        print("❌ 404 Not Found")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "not found",
            "Endpoint or resource not found",
            "Check org, user_id, or path"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(data)

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
    test_get_custom_instruction()