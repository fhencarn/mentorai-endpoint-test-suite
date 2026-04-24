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

ENDPOINT_PATH = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentor-with-settings/"
POST_URL = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentor-with-settings/"

payload = {
    "template_name": "default",
    "new_mentor_name": "Endpoint Test Mentor With Settings",
    "display_name": "Endpoint Test Mentor With Settings",
    "description": "Test mentor created from template with settings.",
    "initial_message": "Hello, I am a test mentor.",
    "suggested_message": "How can I help you today?",
    "theme": "light",
    "user_message_color": "#D9781E",
    "mentor_bubble_color": "#F5F5F5",
    "align_mentor_bubble": "left",
    "system_prompt": "You are a helpful test mentor.",
    "llm_provider": "openai",
    "llm_name": "gpt-4o-mini",
    "mentor_visibility": "viewable_by_tenant_students",
    "enable_image_generation": False,
    "enable_web_browsing": False,
    "enable_code_interpreter": False,
    "metadata": {
        "test": "true"
    },
    "custom_css": "",
    "proactive_message": "Let me know if you need help.",
    "tool_slugs": [],
    "llm_temperature": 0.2,
    "seo_tags": "",
    "marketing_conversations": "",
    "proactive_prompt": "Offer help when appropriate."
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


def test_post_ai_mentor_with_settings():

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
            "Mentor with settings created successfully",
            "Endpoint accepted template and settings payload"
        )
        print("\n--main--")

    elif status == 400:
        print_matrix_row(
            status,
            "bad request",
            response_body,
            "Payload may contain invalid template_name, settings values, or required field formatting"
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
            "Template mentor may not exist or org/user path may be invalid"
        )
        print("\n--secondary--")

    elif status == 405:
        print_matrix_row(
            status,
            "method not allowed",
            response_body,
            "Docs may list POST, but Syracuse environment may expect a different method"
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
    test_post_ai_mentor_with_settings()