import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
MENTOR_SLUG = os.getenv("MENTOR_SLUG")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_mentor_detail():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/mentors/{mentor}/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN or API_KEY in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    if not MENTOR_SLUG:
        print("❌ Missing MENTOR_SLUG in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/mentors/{MENTOR_SLUG}/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Running Test: GET Mentor Detail")
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
        name = data.get("name")
        unique_id = data.get("unique_id")
        slug = data.get("slug")
        platform = data.get("platform")
        allow_anonymous = data.get("allow_anonymous")
        enable_moderation = data.get("enable_moderation")
        is_proactive = data.get("is_proactive")

        response_summary = f"Mentor detail returned for slug={slug}"
        notes = (
            f"Validated mentor detail endpoint; name={name}, unique_id={unique_id}, "
            f"platform={platform}, allow_anonymous={allow_anonymous}, "
            f"enable_moderation={enable_moderation}, is_proactive={is_proactive}"
        )

        print("✅ SUCCESS")
        print(f"Name: {name}")
        print(f"Slug: {slug}")
        print(f"Unique ID: {unique_id}")
        print(f"Platform: {platform}")

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
            "Mentor detail request invalid",
            "Check mentor slug, user_id, or request formatting"
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
            "Access denied",
            "Likely RBAC or tenant restriction"
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
            "Mentor record not found",
            "Check MENTOR_SLUG, user_id, or path"
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
    test_get_mentor_detail()