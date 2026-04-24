import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
ORG = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")

API_KEY = os.getenv("API_KEY")

HEADERS = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json"
}

ENDPOINT_PATH = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentor-from-template/"
POST_URL = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentor-from-template/"

payload = {
    "template_name": "default",
    "new_mentor_name": "Endpoint Test Template Mentor"
}


def safe_text(response):
    try:
        return json.dumps(response.json())
    except Exception:
        return response.text.strip()


def print_matrix_row(status, label, message, notes):
    print(
        f"| ai-mentor | {ENDPOINT_PATH} | POST | ibl.ai docs | "
        f"{status} | {label} | {message} | {notes} |"
    )


def test_post_ai_mentor_from_template():

    if not API_KEY:
        print_matrix_row(
            0,
            "unauthorized",
            "API_KEY not loaded",
            "Missing API key in environment"
        )
        return

    response = requests.put(POST_URL, headers=HEADERS, json=payload)


    status = response.status_code
    response_body = safe_text(response)

    if status == 200:
        print_matrix_row(
            status,
            "working",
            "Mentor created from template successfully",
            "Endpoint accepted template_name and new_mentor_name"
        )
        print("\n--main--")

    elif status == 400:
        print_matrix_row(
            status,
            "bad request",
            response_body,
            "Template name may be invalid or required fields may not match expected values"
        )
        print("\n--secondary--")

    elif status == 401:
        print_matrix_row(
            status,
            "unauthorized",
            response_body,
            "Invalid or missing API token"
        )
        print("\n--secondary--")

    elif status == 403:
        print_matrix_row(
            status,
            "forbidden",
            response_body,
            "Endpoint is restricted to tenant admins"
        )
        print("\n--secondary--")

    elif status == 404:
        print_matrix_row(
            status,
            "not found",
            response_body,
            "Check org, user_id, or template name"
        )
        print("\n--secondary--")

    else:
        print_matrix_row(
            status,
            "error",
            response_body,
            "Unexpected response"
        )
        print("\n--secondary--")

    print("\n--- DEBUG ---")
    print("POST URL:", POST_URL)
    print("Payload:", json.dumps(payload, indent=2))
    print("Response:", response.text)


if __name__ == "__main__":
    test_post_ai_mentor_from_template()