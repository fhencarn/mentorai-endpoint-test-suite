import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"

# Optional filters
SESSION_ID = None   # example: "uuid-here"
USERNAME = None     # example: "fernando"


def test_get_ai_account_tokens():
    endpoint = f"/api/ai-account/orgs/{ORG}/tokens/"
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json",
    }

    params = {}
    if SESSION_ID:
        params["session_id"] = SESSION_ID
    if USERNAME:
        params["username"] = USERNAME

    response = requests.get(url, headers=headers, params=params)

    print("Status Code:", response.status_code)

    try:
        response_summary = response.json()
        print("Response JSON:", response_summary)
    except Exception:
        response_summary = response.text
        print("Response Text:", response_summary)

    if response.status_code == 200:
        label = "working"
        if isinstance(response_summary, list):
            summary = f"{len(response_summary)} token record(s) returned"
            notes = "Auth successful; returned token usage list."
        else:
            summary = "Token data returned"
            notes = "Auth successful; returned token usage data."
    elif response.status_code == 400:
        label = "bad request"
        summary = str(response_summary)[:200]
        notes = "Invalid query params (session_id or username)."
    elif response.status_code == 401:
        label = "unauthorized"
        summary = str(response_summary)[:200]
        notes = "Check API_KEY or Authorization header."
    elif response.status_code == 403:
        label = "forbidden"
        summary = str(response_summary)[:200]
        notes = "Accessible to tenant admins only; token may lack admin permissions."
    elif response.status_code == 404:
        label = "not found"
        summary = str(response_summary)[:200]
        notes = "Org or session_id not found."
    else:
        label = "error"
        summary = str(response_summary)[:200]
        notes = "Unexpected response; check filters, org, or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint} | GET | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_get_ai_account_tokens()