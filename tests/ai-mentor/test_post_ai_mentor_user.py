import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.iblai.app"
ORG = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")

API_KEY = os.getenv("API_KEY")
API_KEY = API_KEY.strip().strip('"').strip("'") if API_KEY else None

HEADERS = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json"
}

ENDPOINT_PATH = "/api/ai-mentor/orgs/{org}/users/{user_id}/"
POST_URL = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/"

# Minimal test flow
flow_json = {
    "name": "Endpoint Test Flow",
    "description": "Minimal Langflow test flow",
    "data": {
        "nodes": [
            {
                "id": "1",
                "type": "PromptNode",
                "position": {"x": 100, "y": 100},
                "data": {
                    "id": "1",
                    "type": "prompt",
                    "node": {
                        "display_name": "Prompt",
                        "description": "Simple test prompt",
                        "template": {
                            "template": {
                                "type": "str",
                                "value": "Hello world"
                            }
                        }
                    }
                }
            }
        ],
        "edges": [],
        "viewport": {"x": 0, "y": 0, "zoom": 1}
    }
}

payload = {
    "name": "Endpoint Test Mentor",
    "slug": "endpoint-test-mentor",
    "flow": flow_json,
    "platform": "syracuse",
    "allow_anonymous": False,
    "metadata": {"test": "true"},
    "enable_moderation": False,
    "is_proactive": False,
    "proactive_prompt": "Test proactive prompt.",
    "moderation_system_prompt": "Test moderation system prompt.",
    "moderation_response": "Test moderation response.",
    "proactive_message": None,
    "created_by": None
}


def safe_text(response):
    try:
        return json.dumps(response.json())
    except Exception:
        return response.text.strip()


def print_matrix_row(status, error_type, message, notes, details):
    print(
        f"| ai-mentor | {ENDPOINT_PATH} | POST | ibl.ai docs | "
        f"{status} | {error_type} | {message} | {notes} | {details} |"
    )


# Step 1: make sure API key exists
if not API_KEY:
    print_matrix_row(
        0,
        "unauthorized",
        "API_KEY not loaded",
        "Request could not be sent because API_KEY was missing from environment",
        "Authentication setup failed before request"
    )
    print("\n--- DEBUG ---")
    print("Loaded API_KEY:", repr(API_KEY))

else:
    # Step 2: auth test against a known endpoint
    auth_test_url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/sessions/"
    auth_response = requests.get(auth_test_url, headers=HEADERS)

    if auth_response.status_code == 401:
        print_matrix_row(
            401,
            "unauthorized",
            safe_text(auth_response),
            "Request failed due to invalid or unread API token",
            "Authentication failed before payload validation"
        )
        print("\n--- DEBUG ---")
        print("BASE_URL:", BASE_URL)
        print("ORG:", ORG)
        print("USER_ID:", USER_ID)
        print("API_KEY repr:", repr(API_KEY))
        print("Authorization header repr:", repr(HEADERS["Authorization"]))
        print("Auth test URL:", auth_test_url)
        print("Auth response:", auth_response.text)

    else:
        # Step 3: run POST test
        response = requests.post(POST_URL, headers=HEADERS, json=payload)
        status = response.status_code
        response_body = safe_text(response)

        if status in [200, 201]:
            print_matrix_row(
                status,
                "success",
                "Mentor created successfully",
                "Endpoint accepts valid mentor creation payload",
                "Request succeeded with valid authentication and non-blank moderation fields"
            )
            print("\n--main--")

        elif status == 400:
            print_matrix_row(
                status,
                "bad request",
                response_body,
                "Request failed due to invalid payload or schema",
                "Endpoint rejected one or more request fields"
            )
            print("\n--secondary--")

        elif status == 401:
            print_matrix_row(
                status,
                "unauthorized",
                response_body,
                "Request failed due to invalid or missing API token",
                "Authentication error occurred before payload validation"
            )
            print("\n--secondary--")

        elif status == 403:
            print_matrix_row(
                status,
                "forbidden",
                response_body,
                "Authenticated, but user does not have permission",
                "Access denied for this resource"
            )
            print("\n--secondary--")

        elif status == 404:
            print_matrix_row(
                status,
                "not found",
                response_body,
                "Endpoint or resource not found",
                "Check org, user_id, or endpoint path"
            )
            print("\n--secondary--")

        else:
            print_matrix_row(
                status,
                "error",
                response_body,
                "Request failed",
                "Unexpected response returned by server"
            )
            print("\n--secondary--")

        print("\n--- DEBUG ---")
        print("POST URL:", POST_URL)
        print("Payload:", json.dumps(payload, indent=2))
        print("Response:", response.text)