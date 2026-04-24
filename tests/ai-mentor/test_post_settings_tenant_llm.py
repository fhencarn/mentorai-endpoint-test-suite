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


def test_post_settings_tenant_llm():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/settings/tenant-llm/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/settings/tenant-llm/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "llm_provider": "openai",
        "llm_name": "gpt-4o-mini"
    }

    print("\n--- DEBUG ---")
    print("POST URL:", url)
    print("USER_ID:", USER_ID)
    print("Payload:")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        status = response.status_code

        try:
            response_json = response.json()
            response_summary = json.dumps(response_json)[:220]
        except ValueError:
            response_json = None
            response_summary = response.text[:220].replace("\n", " ")

        print("Status Code:", status)
        print("Response:", response_summary)

        if status == 201:
            label = "working"
            notes = "Validated tenant LLM creation endpoint; tenant LLM record created successfully."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but payload may be invalid; verify llm_provider and llm_name values."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token and whether this endpoint is tenant-admin only."
        elif status == 403:
            label = "forbidden"
            notes = "User-role test indicates this endpoint is permission-restricted, likely tenant-admin only."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but org/user context could not be resolved."
        else:
            label = "error"
            notes = "Unexpected response; check payload, permissions, or server behavior."

        print_matrix_row(
            section="ai-mentor",
            endpoint=endpoint_template,
            method="POST",
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
            method="POST",
            doc_source="ibl.ai docs",
            status="N/A",
            label="error",
            response_summary=str(e),
            notes="Script/runtime failure while testing settings/tenant-llm endpoint.",
        )


if __name__ == "__main__":
    test_post_settings_tenant_llm()