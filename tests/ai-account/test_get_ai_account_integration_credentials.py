import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"

# Optional filter; leave as None to return all integration credentials
CREDENTIAL_NAME = None  # example: "google-drive"


def test_get_ai_account_integration_credentials():
    endpoint = f"/api/ai-account/orgs/{ORG}/integration-credential/"
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
            summary = f"{len(response_summary)} integration credential(s) returned"
            notes = "Auth successful; returned integration credential list."
        else:
            summary = "Integration credential response returned"
            notes = "Auth successful; returned integration credential data."
    elif response.status_code == 400:
        label = "bad request"
        summary = str(response_summary)[:200]
        notes = "Request reached endpoint, but query parameter may be invalid."
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
        notes = "Check org value or credential name if filtering."
    else:
        label = "error"
        summary = str(response_summary)[:200]
        notes = "Unexpected response; check org, token permissions, or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint} | GET | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_get_ai_account_integration_credentials()