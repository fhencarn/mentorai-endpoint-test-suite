import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
FEEDBACK_ID = os.getenv("FEEDBACK_ID")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_mentor_feedback_by_id():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentor-feedback/{feedback_id}/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not FEEDBACK_ID:
        print("❌ Missing FEEDBACK_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentor-feedback/{FEEDBACK_ID}/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: GET Mentor Feedback by ID")
    print(f"URL: {url}")

    response = requests.get(url, headers=headers)
    status_code = response.status_code

    try:
        data = response.json()
    except Exception:
        print("❌ Response is not JSON")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "error",
            "Non-JSON response returned",
            "Failed to parse response body"
        )
        return False

    if status_code == 200:
        feedback_id = data.get("id")
        username = data.get("username")
        session = data.get("session")
        rating = data.get("rating")
        mentor = data.get("mentor")

        user_text_status = "present" if data.get("user_text") not in [None, ""] else "empty"
        ai_response_status = "present" if data.get("ai_response") not in [None, ""] else "empty"
        reason_status = "present" if data.get("reason") not in [None, ""] else "empty"
        additional_feedback_status = "present" if data.get("additional_feedback") not in [None, ""] else "empty"

        response_summary = f"Mentor feedback {feedback_id} returned"
        notes = (
            f"Validated feedback detail endpoint; username={username}, session={session}, "
            f"rating={rating}, mentor={mentor}, user_text={user_text_status}, "
            f"ai_response={ai_response_status}, reason={reason_status}, "
            f"additional_feedback={additional_feedback_status}"
        )

        print("✅ SUCCESS")
        print(f"ID: {feedback_id}")
        print(f"Username: {username}")
        print(f"Session: {session}")
        print(f"Rating: {rating}")
        print(f"Mentor: {mentor}")
        print(f"User Text: {user_text_status}")
        print(f"AI Response: {ai_response_status}")
        print(f"Reason: {reason_status}")
        print(f"Additional Feedback: {additional_feedback_status}")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "working",
            response_summary,
            notes
        )
        return True

    elif status_code == 400:
        print("❌ 400 Bad Request")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "bad request",
            "Feedback request invalid",
            "Check feedback_id format, user_id, or request data"
        )
        return False

    elif status_code == 401:
        print("❌ 401 Unauthorized")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "auth failed",
            "Authentication failed",
            "Invalid or missing API token"
        )
        return False

    elif status_code == 403:
        print("❌ 403 Forbidden")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Request authenticated but access denied",
            "Likely RBAC or org/user permission restriction"
        )
        return False

    elif status_code == 404:
        print("❌ 404 Not Found")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "not found",
            "Feedback record not found",
            "Likely FEEDBACK_ID is invalid or no feedback exists for this user"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Unexpected response returned",
            "Manual review recommended"
        )
        return False


if __name__ == "__main__":
    test_get_mentor_feedback_by_id()