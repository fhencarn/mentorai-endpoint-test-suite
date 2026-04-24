import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

FEEDBACK_ID = os.getenv("FEEDBACK_ID")
SESSION_ID = os.getenv("SESSION_ID")
MENTOR_NUMERIC_ID = os.getenv("MENTOR_NUMERIC_ID", "1")
USERNAME = os.getenv("USERNAME", USER_ID)


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


def test_put_mentor_feedback():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentor-feedback/{feedback_id}/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentor-feedback/{FEEDBACK_ID}/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "username": USERNAME,
        "session": str(SESSION_ID),
        "user_text": "Endpoint matrix PUT test user message.",
        "ai_response": "Endpoint matrix PUT test AI response.",
        "reason": "Testing mentor feedback update endpoint.",
        "additional_feedback": "Update test completed.",
        "rating": 1,
        "mentor": int(MENTOR_NUMERIC_ID),
    }

    print("\n--- DEBUG ---")
    print("PUT URL:", url)
    print("USER_ID:", USER_ID)
    print("FEEDBACK_ID:", FEEDBACK_ID)
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
            notes = "Validated mentor feedback update endpoint; feedback object returned successfully after PUT request."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but payload may be invalid; verify feedback_id, session, mentor, and required text fields."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token."
        elif status == 403:
            label = "forbidden"
            notes = "Endpoint is permission-restricted for this user context."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but the provided feedback_id or related resource could not be resolved."
        else:
            label = "error"
            notes = "Unexpected response; check payload, feedback_id, or server behavior."

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
            notes="Script/runtime failure while testing mentor-feedback endpoint.",
        )


if __name__ == "__main__":
    test_put_mentor_feedback()