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


def test_post_predictive_analytics():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/predictive-analytics/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/predictive-analytics/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "prompt": {
            "data_variables": [
                {
                    "variable_name": "registered_users",
                    "data_set": {
                        "2026-04-01": 4,
                        "2026-04-02": 6,
                        "2026-04-03": 5,
                        "2026-04-04": 7,
                        "2026-04-05": 8
                    },
                    "number_of_data_points": 3
                }
            ]
        }
    }

    print("\n--- DEBUG ---")
    print("POST URL:", url)
    print("USER_ID:", USER_ID)
    print("Payload:")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        status = response.status_code

        try:
            response_json = response.json()
            response_summary = json.dumps(response_json)[:220]
        except ValueError:
            response_json = None
            response_summary = response.text[:220].replace("\n", " ")

        print("Status Code:", status)
        print("Response:", response_summary)

        if status == 200:
            label = "working"
            notes = "Validated predictive analytics endpoint; predictive data returned successfully."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but AI response could not be parsed to JSON or payload format may be invalid."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token and whether this endpoint is restricted to tenant admins."
        elif status == 403:
            label = "forbidden"
            notes = "User-role test indicates this endpoint is permission-restricted, likely tenant-admin only."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but tenant OpenAI key may not be configured or org/user context could not be resolved."
        elif status == 429:
            label = "rate limited"
            notes = "OpenAI request exceeded the rate limit during predictive analytics processing."
        else:
            label = "error"
            notes = "Unexpected response; check payload, permissions, tenant OpenAI configuration, or server behavior."

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
            notes="Script/runtime failure while testing predictive-analytics endpoint.",
        )


if __name__ == "__main__":
    test_post_predictive_analytics()