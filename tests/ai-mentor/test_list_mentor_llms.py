import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_list_mentor_llms():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentor-llms/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentor-llms/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: LIST Mentor LLMs")
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
        if isinstance(data, list):
            count = len(data)

            sample_fields = []
            if count > 0:
                first = data[0]
                expected_keys = [
                    "id", "name", "description", "metadata",
                    "resource_ids", "tags", "overview",
                    "use_cases", "documentation", "chat_models", "logo"
                ]
                sample_fields = [k for k in expected_keys if k in first]

            response_summary = f"{count} LLM(s) returned"
            notes = f"Validated mentor LLM list endpoint; sample fields present: {', '.join(sample_fields) if sample_fields else 'none'}"

            print("✅ SUCCESS")
            print(f"LLMs Returned: {count}")

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

        else:
            print("❌ Unexpected structure (not a list)")
            print(data)

            print_matrix_row(
                "ai-mentor",
                endpoint_template,
                "GET",
                "ibl.ai docs",
                status_code,
                "review needed",
                "Response not in expected list format",
                "Expected list of LLM objects"
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
            "Access denied",
            "Likely RBAC or tenant restriction"
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
    test_list_mentor_llms()