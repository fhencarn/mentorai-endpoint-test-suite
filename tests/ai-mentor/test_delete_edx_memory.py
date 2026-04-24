import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")
EDX_MEMORY_ID = os.getenv("EDX_MEMORY_ID")


def label_status(status_code):
    labels = {
        204: "working",
        400: "bad request",
        401: "unauthorized",
        403: "forbidden",
        404: "not found",
        405: "method not allowed",
    }
    return labels.get(status_code, "review needed")


def clean(value):
    return str(value).replace("\n", " ").replace("|", "/")[:300]


def test_delete_edx_memory():
    actual_endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/edx-memory/{EDX_MEMORY_ID}/"
    matrix_endpoint = "/api/ai-mentor/orgs/{org}/users/{user_id}/edx-memory/{id}/"
    url = f"{BASE_URL}{actual_endpoint}"

    headers = {
        "Authorization": f"Token {API_KEY}",
    }

    response = requests.delete(url, headers=headers)
    status = response.status_code
    label = label_status(status)

    try:
        data = response.json()
    except ValueError:
        data = response.text or "No response body"

    if status == 204:
        summary = "EdX memory deleted successfully"
        notes = "Validated DELETE edx-memory endpoint; returned 204 No Content"

    elif status == 400:
        summary = "Bad request"
        notes = f"Check request structure; response={clean(data)}"

    elif status == 401:
        summary = "Authentication failed"
        notes = "Check API_KEY or Authorization header format"

    elif status == 403:
        summary = "Permission denied"
        notes = "Current user role may not allow deleting EdX memory"

    elif status == 404:
        summary = "EdX memory not found"
        notes = "Check org, user_id, or edx memory id"

    elif status == 405:
        summary = "DELETE method not allowed"
        notes = "Verify endpoint supports DELETE"

    else:
        summary = "Unexpected response"
        notes = clean(data)

    print(
        f"| ai-mentor | {matrix_endpoint} | DELETE | ibl.ai docs | {status} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_delete_edx_memory()