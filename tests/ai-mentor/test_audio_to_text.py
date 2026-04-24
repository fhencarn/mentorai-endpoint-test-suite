import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_KEY")

AUDIO_FILE_PATH = os.getenv("AUDIO_FILE_PATH", "test_audio.wav")


# ========================
# MATRIX OUTPUT HELPERS
# ========================
def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


# ========================
# TEST FUNCTION
# ========================
def test_audio_to_text():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/audio-to-text/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/audio-to-text/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}"
        # ⚠️ DO NOT set Content-Type manually for file upload
    }

    print("🔍 Running Test: POST Audio to Text")
    print(f"URL: {url}")

    files = {
        "file": open(AUDIO_FILE_PATH, "rb")
    }

    response = requests.post(url, headers=headers, files=files)
    status_code = response.status_code

    try:
        data = response.json()
    except Exception:
        print("❌ Response is not JSON")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "error",
            "Non-JSON response returned",
            "Failed to parse response"
        )
        return False

    # ========================
    # SUCCESS CASE
    # ========================
    if status_code == 200:
        text = data.get("text", "")

        response_summary = "Audio successfully converted to text"
        notes = f"Returned text length: {len(text)} characters"

        print("✅ SUCCESS")
        print(f"Transcript: {text}")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "working",
            response_summary,
            notes
        )
        return True

    # ========================
    # ERROR CASES
    # ========================
    elif status_code == 400:
        print("❌ 400 Bad Request")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "bad request",
            "Invalid or missing audio file",
            "Check file format or request structure"
        )
        return False

    elif status_code == 401:
        print("❌ 401 Unauthorized")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
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
            "POST",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Access denied",
            "Likely RBAC restriction"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Unexpected response",
            "Manual review required"
        )
        return False


# ========================
# RUN TEST
# ========================
if __name__ == "__main__":
    test_audio_to_text()