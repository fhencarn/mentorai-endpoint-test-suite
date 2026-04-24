import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")
SCRIPT_ID = os.getenv("SCRIPT_ID")


def label_status(status_code):
    labels = {
        200: "working",
        400: "bad request",
        401: "unauthorized",
        403: "forbidden",
        404: "not found / invalid id",
        405: "method not allowed",
    }
    return labels.get(status_code, "review needed")


def clean(value):
    return str(value).replace("\n", " ").replace("|", "/")[:300]


def test_patch_playwright_script():
    actual_endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/playwright-scripts/{SCRIPT_ID}/"
    matrix_endpoint = "/api/ai-mentor/orgs/{org}/users/{user_id}/playwright-scripts/{id}/"
    url = f"{BASE_URL}{actual_endpoint}"

    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {}  # minimal payload per docs

    response = requests.patch(url, headers=headers, json=payload)
    status = response.status_code
    label = label_status(status)

    try:
        data = response.json()
    except ValueError:
        data = response.text

    if status == 200 and isinstance(data, dict):
        script_id = data.get("id", "N/A")
        title = data.get("title", "")
        is_public = data.get("is_public", "N/A")

        summary = f"Playwright script updated: id={script_id}, public={is_public}"
        notes = f"Validated PATCH playwright script endpoint; title='{title or 'empty'}'"

    elif status == 400:
        summary = "Invalid playwright script payload"
        notes = f"Check payload fields; response={clean(data)}"

    elif status == 401:
        summary = "Authentication failed"
        notes = "Check API_KEY or Authorization header format"

    elif status == 403:
        summary = "Permission denied"
        notes = "User role may not allow updating playwright scripts"

    elif status == 404:
        summary = "Playwright script not found"
        notes = "Check org, user_id, or script id"

    elif status == 405:
        summary = "PATCH method not allowed"
        notes = "Verify endpoint supports PATCH"

    else:
        summary = "Unexpected response"
        notes = clean(data)

    print(
        f"| ai-mentor | {matrix_endpoint} | PATCH | ibl.ai docs | {status} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_patch_playwright_script()