import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")


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


def test_put_custom_instruction():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/custom-instruction/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/custom-instruction/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "about_user": "This is a test user for endpoint validation.",
        "mentor_tone": "friendly"
    }

    print("\n--- DEBUG ---")
    print("PUT URL:", url)
    print("USER_ID:", USER_ID)
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
            notes = "Validated custom instruction update endpoint; about_user and mentor_tone updated successfully."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but payload may be invalid; verify required fields."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token."
        elif status == 403:
            label = "forbidden"
            notes = "Endpoint is permission-restricted for this user context."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but org/user context could not be resolved."
        else:
            label = "error"
            notes = "Unexpected response; check payload or server behavior."

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
            notes="Script/runtime failure while testing custom-instruction endpoint.",
        )


if __name__ == "__main__":
    test_put_custom_instruction()