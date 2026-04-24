import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

PLAYWRIGHT_SCRIPT_ID = os.getenv("PLAYWRIGHT_SCRIPT_ID", "1")


def get_auth_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def print_matrix_row(section, endpoint, method, doc_source, status, label, response_summary, notes):
    print(
        f"| {section} | {endpoint} | {method} | {doc_source} | "
        f"{status} | {label} | {response_summary} | {notes} |"
    )


def test_put_playwright_script():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/playwright-scripts/{id}/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/playwright-scripts/{PLAYWRIGHT_SCRIPT_ID}/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "title": "Endpoint Test Playwright Script Updated",
        "description": "Updated by endpoint matrix PUT test.",
        "script": "console.log('Updated MentorAI endpoint test playwright script');"
    }

    print("\n--- DEBUG ---")
    print("PUT URL:", url)
    print("USER_ID:", USER_ID)
    print("PLAYWRIGHT_SCRIPT_ID:", PLAYWRIGHT_SCRIPT_ID)
    print("Payload:")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.put(url, headers=headers, json=payload, timeout=30)
        status = response.status_code

        try:
            response_json = response.json()
            response_summary = json.dumps(response_json)[:220]
        except ValueError:
            response_summary = response.text[:220].replace("\n", " ")

        print("Status Code:", status)
        print("Response:", response_summary)

        if status == 200:
            label = "working"
            notes = "Validated playwright script update endpoint; script record returned successfully after PUT request."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but payload may be invalid; verify title, description, and script formatting."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token."
        elif status == 403:
            label = "forbidden"
            notes = "Endpoint is permission-restricted for this user context."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but the provided playwright script ID could not be resolved."
        else:
            label = "error"
            notes = "Unexpected response; check payload, script ID, permissions, or server behavior."

        print_matrix_row(
            section="ai-mentor",
            endpoint=endpoint_template,
            method="PUT",
            doc_source="ibl.ai docs",
            status=status,
            label=label,
            response_summary=response_summary,
            notes=notes,
        )

    except Exception as e:
        print_matrix_row(
            section="ai-mentor",
            endpoint=endpoint_template,
            method="PUT",
            doc_source="ibl.ai docs",
            status="N/A",
            label="error",
            response_summary=str(e),
            notes="Script/runtime failure while testing playwright-scripts update endpoint.",
        )


if __name__ == "__main__":
    test_put_playwright_script()