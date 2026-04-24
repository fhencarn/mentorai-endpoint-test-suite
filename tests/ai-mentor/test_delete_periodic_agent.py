import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")
PERIODIC_AGENT_ID = os.getenv("PERIODIC_AGENT_ID")


def label_status(status_code):
    labels = {
        204: "working",
        400: "bad request",
        401: "unauthorized",
        403: "forbidden",
        404: "not found / invalid id",
        405: "method not allowed",
    }
    return labels.get(status_code, "review needed")


def clean(value):
    return str(value).replace("\n", " ").replace("|", "/")[:300]


def test_delete_periodic_agent():
    actual_endpoint = f"/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/periodic-agents/{PERIODIC_AGENT_ID}/"
    matrix_endpoint = "/api/ai-mentor/orgs/{org}/users/{user_id}/periodic-agents/{id}/"
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
        summary = "Periodic agent deleted successfully"
        notes = "Validated DELETE periodic agent endpoint; returned 204 No Content"

    elif status == 400:
        summary = "Bad request"
        notes = f"Check request structure; response={clean(data)}"

    elif status == 401:
        summary = "Authentication failed"
        notes = "Check API_KEY or Authorization header format"

    elif status == 403:
        summary = "Permission denied"
        notes = "Endpoint restricted to platform admins and tenant administrators"

    elif status == 404:
        summary = "Periodic agent not found"
        notes = "Check org, user_id, or periodic agent id"

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
    test_delete_periodic_agent()