import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from dotenv import load_dotenv
from utils.auth import get_access_token
from utils.matrix import print_matrix_row

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")

def test_ai_prompt_memory():
    endpoint = f"/api/ai-prompt/orgs/{ORG}/users/{USER_ID}/memory/"
    url = f"{BASE_URL}{endpoint}"

    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    try:
        data = response.json()
    except Exception:
        data = response.text

    status = response.status_code

    if status == 200:
        label = "working"
        summary = "Catalog item memory retrieved successfully"
        notes = "Endpoint returned user catalog memory data"
    elif status == 400:
        label = "working-needs-docs"
        summary = "Request failed due to missing or invalid parameters"
        notes = "Check docs for required path or query parameters"
    elif status == 401:
        label = "unknown"
        summary = "Authentication failed"
        notes = "Token may be missing or invalid"
    elif status == 403:
        label = "permission-restricted"
        summary = "Request authenticated but access denied"
        notes = "Likely restricted by read-only role or tenant permissions"
    elif status == 404:
        label = "working"
        summary = "No catalog memory found for this user"
        notes = "Docs indicate NotFound may occur if no memory exists"
    elif status >= 500:
        label = "server-error"
        summary = "Server returned an internal error"
        notes = "Backend issue likely"
    else:
        label = "unknown"
        summary = "Unexpected response"
        notes = "Needs manual review"

    print("Status:", status)
    print("Response:", data)

    print_matrix_row(
        "ai-prompt",
        endpoint,
        "GET",
        "IBL.ai.docs",
        status,
        label,
        summary,
        notes
    )

if __name__ == "__main__":
    test_ai_prompt_memory()