import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
TASK_ID = os.getenv("TASK_ID")
API_TOKEN = os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_download_task_by_id():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/downloads/tasks/{task_id}/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not TASK_ID:
        print("❌ Missing TASK_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/downloads/tasks/{TASK_ID}/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: GET Download Task by ID")
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
        # Case 1: task not ready yet
        if data.get("state") == "task_not_ready":
            response_summary = "Download task checked; task_not_ready returned"
            notes = "Validated task lookup endpoint; task exists but output is not ready yet"

            print("✅ SUCCESS")
            print("Task State: task_not_ready")

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

        # Case 2: chat history object returned
        content_type = data.get("type")
        timestamp = data.get("timestamp")
        has_content = "present" if data.get("content") not in [None, ""] else "empty"

        response_summary = (
            f"Download task returned chat history object: "
            f"type={content_type}, content={has_content}, timestamp={timestamp}"
        )
        notes = "Validated task lookup endpoint and returned expected download object fields"

        print("✅ SUCCESS")
        print(f"Type: {content_type}")
        print(f"Timestamp: {timestamp}")
        print(f"Content Present: {has_content}")

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

    elif status_code == 400:
        print("❌ 400 Bad Request")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "bad request",
            "Task request invalid",
            "Check task_id format or request data"
        )
        return False

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
            "Task or endpoint not found",
            "Check org, user_id, task_id, or path"
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
    test_get_download_task_by_id()