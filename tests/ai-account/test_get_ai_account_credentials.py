import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"

# Optional filter; leave as None to return all credentials
CREDENTIAL_NAME = None  # example: "openai"


def test_get_ai_account_credentials():
    endpoint = f"/api/ai-account/orgs/{ORG}/credential/"
    url = f"{BASE_URL}{endpoint}"

    headers = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json",
}

    params = {}
    if CREDENTIAL_NAME:
        params["name"] = CREDENTIAL_NAME

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
            notes = f"Auth successful; returned {len(response_summary)} credential(s)."
            summary = f"{len(response_summary)} credential(s) returned"
        elif isinstance(response_summary, dict):
            notes = "Auth successful; returned credential response."
            summary = "Credential response returned"
        else:
            notes = "Auth successful; returned credential data."
            summary = "Credential data returned"
    elif response.status_code == 400:
        label = "bad request"
        notes = "Request reached endpoint, but query parameter may be invalid."
        summary = str(response_summary)[:200]
    elif response.status_code == 401:
        label = "unauthorized"
        notes = "Check API_KEY or Authorization header."
        summary = str(response_summary)[:200]
    elif response.status_code == 403:
        label = "forbidden"
        notes = "Accessible to tenant admins only; token may lack admin permissions."
        summary = str(response_summary)[:200]
    elif response.status_code == 404:
        label = "not found"
        notes = "Check org value or credential name if filtering."
        summary = str(response_summary)[:200]
    else:
        label = "error"
        notes = "Unexpected response; check org, token permissions, or server behavior."
        summary = str(response_summary)[:200]

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint} | GET | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_get_ai_account_credentials()