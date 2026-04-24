import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

PERIODIC_AGENT_ID = os.getenv("PERIODIC_AGENT_ID", "1")
MENTOR_NUMERIC_ID = os.getenv("MENTOR_NUMERIC_ID", "1")


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


def test_put_periodic_agent():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/periodic-agents/{id}/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/periodic-agents/{PERIODIC_AGENT_ID}/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "mentor": int(MENTOR_NUMERIC_ID),
        "title": "Endpoint Test Periodic Agent Updated",
        "description": "Updated by endpoint matrix PUT test.",
        "prompt": "Run an updated periodic summary check.",
        "task": {
            "crontab": {
                "minute": "0",
                "hour": "9",
                "day_of_week": "*",
                "day_of_month": "*",
                "month_of_year": "*"
            }
        }
    }

    print("\n--- DEBUG ---")
    print("PUT URL:", url)
    print("USER_ID:", USER_ID)
    print("PERIODIC_AGENT_ID:", PERIODIC_AGENT_ID)
    print("MENTOR_NUMERIC_ID:", MENTOR_NUMERIC_ID)
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
            notes = "Validated periodic agent update endpoint; periodic agent returned successfully after PUT request."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but payload may be invalid; verify mentor ID, title, and crontab structure."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token."
        elif status == 403:
            label = "forbidden"
            notes = "User-role test indicates this endpoint is permission-restricted, likely platform-admin or tenant-admin only."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but the provided periodic agent ID or related resource could not be resolved."
        else:
            label = "error"
            notes = "Unexpected response; check payload, periodic agent ID, permissions, or server behavior."

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
            notes="Script/runtime failure while testing periodic-agents update endpoint.",
        )


if __name__ == "__main__":
    test_put_periodic_agent()