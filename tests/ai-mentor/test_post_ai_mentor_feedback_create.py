import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
ORG = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")

API_KEY = os.getenv("API_KEY")
API_KEY = API_KEY.strip().strip('"').strip("'") if API_KEY else None

HEADERS = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json"
}

ENDPOINT_PATH = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentor-feedback/create/"
POST_URL = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentor-feedback/create/"

payload = {
    "username": USER_ID,
    "session": 1,
    "user_text": "This is a test user message.",
    "ai_response": "This is a test AI response.",
    "reason": "helpful",
    "additional_feedback": "Test feedback submitted through endpoint test.",
    "mentor": "2262954f-95c1-4a9c-8943-bd3e9f58b3df",
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


def test_post_ai_mentor_feedback_create():

    if not API_KEY:
        print_matrix_row(
            0,
            "unauthorized",
            "API_KEY not loaded",
            "Missing API key in environment"
        )
        return

    response = requests.post(POST_URL, headers=HEADERS, json=payload)

    status = response.status_code
    response_body = safe_text(response)

    if status in [200, 201]:
        print_matrix_row(
            status,
            "working",
            "Mentor feedback created successfully",
            "Endpoint accepted feedback payload and returned created object"
        )
        print("\n--main--")

    elif status == 400:
        print_matrix_row(
            status,
            "bad request",
            response_body,
            "Payload may contain invalid session, mentor, or required field values"
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
            "Authenticated but user does not have permission"
        )
        print("\n--secondary--")

    elif status == 404:
        print_matrix_row(
            status,
            "not found",
            response_body,
            "Check org, user_id, or referenced session/mentor values"
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
    test_post_ai_mentor_feedback_create()