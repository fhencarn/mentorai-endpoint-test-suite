import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from dotenv import load_dotenv
from utils.auth import get_access_token
from utils.matrix import print_matrix_row

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def test_core_orgs_favicon():
    endpoint = "/api/core/orgs/syracuse/favicon/"
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
        summary = "Request succeeded"
        notes = "Endpoint returned a valid response"
    elif status == 400:
        label = "working-needs-docs"
        summary = "Request failed due to missing or invalid parameters"
        notes = "Check docs for required query parameters"
    elif status == 401:
        label = "unknown"
        summary = "Authentication failed"
        notes = "Token may be missing or invalid"
    elif status == 403:
        label = "permission-restricted"
        summary = "Request authenticated but access denied"
        notes = "Likely restricted by read-only role"
    elif status == 404:
        label = "undocumented"
        summary = "Endpoint not found or path may be outdated"
        notes = "Check docs and base path"
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
        "core",
        endpoint,
        "GET",
        "IBL.ai.docs",
        status,
        label,
        summary,
        notes
    )

if __name__ == "__main__":
    test_core_orgs_favicon()