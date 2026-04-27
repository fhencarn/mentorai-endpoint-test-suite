import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"

# Safe placeholder metadata
PLATFORM_METADATA = {
    "llms": {
        "google": {
            "google_project": "NO_PROJECT_ID",
            "google_location": "us-central1"
        }
    }
}


def test_post_ai_account_platform_metadata():
    endpoint_template = "/api/ai-account/orgs/{org}/platform-metadata/"
    endpoint = endpoint_template.format(org=ORG)
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "data": PLATFORM_METADATA
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)

    try:
        response_data = response.json()
        print("Response JSON:", response_data)
    except Exception:
        response_data = response.text
        print("Response Text:", response_data[:300])

    if response.status_code in [200, 201]:
        label = "working"
        summary = "Platform metadata created"
        notes = "Auth successful; created or added platform metadata."
    elif response.status_code == 400:
        label = "bad request"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Request reached endpoint, but metadata payload may be invalid."
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
        notes = "Endpoint reached, but platform metadata or tenant org was not found."
    else:
        label = "error"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Unexpected response; check payload, org, permissions, or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint_template} | POST | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_post_ai_account_platform_metadata()