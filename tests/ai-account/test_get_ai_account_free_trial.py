import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"
USER_ID = "5718e5"  # replace if needed


def test_get_ai_account_free_trial():
    endpoint_template = "/api/ai-account/orgs/{org}/users/{user_id}/free-trial"
    endpoint = endpoint_template.format(org=ORG, user_id=USER_ID)
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
        print("Response Text:", response_data[:300])

    if response.status_code == 200:
        label = "working"
        if isinstance(response_data, dict) and "is_in_free_trial" in response_data:
            summary = f"is_in_free_trial = {response_data.get('is_in_free_trial')}"
            notes = "Auth successful; returned free trial status."
        else:
            summary = "Free trial status returned"
            notes = "Auth successful; returned free trial response."
    elif response.status_code == 400:
        label = "bad request"
        summary = "Invalid request"
        notes = "Check org or user_id format."
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
        summary = "Free trial status not found"
        notes = "Endpoint reached, but free trial status was not found for this org or user."
    else:
        label = "error"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Unexpected response; check org, user_id, permissions, or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint_template} | GET | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_get_ai_account_free_trial()