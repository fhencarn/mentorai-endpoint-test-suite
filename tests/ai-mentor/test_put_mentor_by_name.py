import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

MENTOR_PATH_NAME = os.getenv("MENTOR_PATH_NAME", "Leadership & Involvement MentorAI")
MENTOR_NAME = os.getenv("MENTOR_NAME", "Leadership & Involvement MentorAI")
MENTOR_SLUG = os.getenv("MENTOR_SLUG", "leadership-involvement-mentorai")


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


def test_put_mentor_by_name():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/{name}/"
    endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/{MENTOR_PATH_NAME}/"
    url = f"{BASE_URL}{endpoint}"

    headers = get_auth_headers()

    payload = {
        "name": MENTOR_NAME,
        "flow": {},
        "slug": MENTOR_SLUG
    }

    print("\n--- DEBUG ---")
    print("PUT URL:", url)
    print("USER_ID:", USER_ID)
    print("MENTOR_PATH_NAME:", MENTOR_PATH_NAME)
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
            notes = "Validated mentor update endpoint; mentor returned successfully after PUT request."
        elif status == 400:
            label = "bad request"
            notes = "Request reached endpoint, but payload may be invalid; verify required fields such as name, flow, and slug."
        elif status == 401:
            label = "unauthorized"
            notes = "User-role test failed authorization; verify API token."
        elif status == 403:
            label = "forbidden"
            notes = "Endpoint is permission-restricted for this user context."
        elif status == 404:
            label = "not found"
            notes = "Endpoint reachable, but the provided mentor path name could not be resolved."
        else:
            label = "error"
            notes = "Unexpected response; check payload, mentor name, slug, or server behavior."

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
            notes="Script/runtime failure while testing mentor update endpoint.",
        )


if __name__ == "__main__":
    test_put_mentor_by_name()