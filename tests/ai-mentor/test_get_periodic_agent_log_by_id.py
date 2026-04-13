import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
PERIODIC_AGENT_LOG_ID = os.getenv("PERIODIC_AGENT_LOG_ID")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_periodic_agent_log_by_id():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/periodic-agent-logs/{id}/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not PERIODIC_AGENT_LOG_ID:
        print("❌ Missing PERIODIC_AGENT_LOG_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/periodic-agent-logs/{PERIODIC_AGENT_LOG_ID}/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: GET Periodic Agent Log by ID")
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
        log_id = data.get("id")
        status = data.get("status")
        periodic_agent = data.get("periodic_agent")
        content_status = "present" if data.get("content") not in [None, ""] else "empty"
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        response_summary = f"Periodic agent log {log_id} returned"
        notes = (
            f"Validated periodic agent log detail endpoint; status={status}, "
            f"periodic_agent={periodic_agent}, content={content_status}, "
            f"start_time={start_time}, end_time={end_time}"
        )

        print("✅ SUCCESS")
        print(f"ID: {log_id}")
        print(f"Status: {status}")
        print(f"Periodic Agent: {periodic_agent}")
        print(f"Content: {content_status}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")

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
            "Periodic agent log not found",
            "Check PERIODIC_AGENT_LOG_ID, user_id, or path"
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
    test_get_periodic_agent_log_by_id()