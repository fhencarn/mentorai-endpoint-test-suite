import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")
MENTOR_ID = os.getenv("MENTOR_ID")


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


def test_post_periodic_agents():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/periodic-agents/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/periodic-agents/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "mentor": (MENTOR_ID),
        "title": "Endpoint Test Periodic Agent",
        "description": "Created by endpoint matrix user-role test.",
        "prompt": "Run a periodic summary check.",
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
    print("POST URL:", url)
    print("USER_ID:", USER_ID)
    print("MENTOR_ID:", MENTOR_ID)
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

        if status in (200, 201):
            label = "working"
            notes = "User-role test succeeded; periodic agent created successfully."
        elif status == 401:
            label = "unauthorized"
            notes = (
                "User-role test; endpoint appears restricted to platform admins or tenant "
                "administrators, so this denial is expected for a standard user."
            )
        elif status == 403:
            label = "forbidden"
            notes = (
                "User-role test; endpoint is permission-restricted and not available to a standard user."
            )
        elif status == 400:
            label = "bad request"
            notes = (
                "User-role test reached the endpoint, but payload may be invalid. Verify mentor ID, "
                "required task structure, or cron formatting."
            )
        elif status == 404:
            label = "not found"
            notes = (
                "User-role test could not resolve the requested org, user, or related resource."
            )
        else:
            label = "error"
            notes = "User-role test returned an unexpected response; check payload, permissions, or server behavior."

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
            notes="Script/runtime failure while testing periodic agents endpoint.",
        )


if __name__ == "__main__":
    test_post_periodic_agents()