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

def test_ai_prompt_styles():
    endpoint = f"/api/ai-prompt/orgs/{ORG}/users/{USER_ID}/styles/"
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
        summary = "Prompt styles retrieved successfully"
        notes = "Endpoint returned list of available prompt styles"
    elif status == 400:
        label = "working-needs-docs"
        summary = "Request failed due to missing or invalid parameters"
        notes = "Check required parameters"
    elif status == 401:
        label = "unknown"
        summary = "Authentication failed"
        notes = "Token issue"
    elif status == 403:
        label = "permission-restricted"
        summary = "Access denied"
        notes = "Requires tenant admin/student permissions"
    elif status == 404:
        label = "working-needs-docs"
        summary = "No styles found"
        notes = "Docs unclear if empty list or 404 is expected"
    elif status >= 500:
        label = "server-error"
        summary = "Server error"
        notes = "Backend issue"
    else:
        label = "unknown"
        summary = "Unexpected response"
        notes = "Needs review"

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
    test_ai_prompt_styles()