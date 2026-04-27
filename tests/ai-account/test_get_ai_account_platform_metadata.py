import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"


def test_get_ai_account_platform_metadata():
    endpoint_template = "/api/ai-account/orgs/{org}/platform-metadata/"
    endpoint = endpoint_template.format(org=ORG)
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)

    try:
        response_data = response.json()
        print("Response JSON:", response_data)
    except Exception:
        response_data = response.text
        print("Response Text:", response_data[:500])

    if response.status_code == 200:
        label = "working"
        summary = "Platform metadata returned"
        notes = "Auth successful; returned platform metadata."
    elif response.status_code == 401:
        label = "unauthorized"
        summary = "Invalid or missing token"
        notes = "Check API_KEY or Authorization header."
    elif response.status_code == 403:
        label = "forbidden"
        summary = "Permission denied"
        notes = "Accessible to tenant admins only; token may lack admin permissions."
    elif response.status_code == 404:
        label = "not found"
        summary = "Platform metadata not found"
        notes = "Endpoint reached, but platform metadata was not found for this org."
    else:
        label = "error"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Unexpected response; check org, permissions, or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint_template} | GET | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_get_ai_account_platform_metadata()