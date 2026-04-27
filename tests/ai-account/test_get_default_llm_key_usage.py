import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"
USER_ID = "5718e5"  # replace if needed


def test_get_default_llm_key_usage():
    endpoint_template = "/api/ai-account/orgs/{org}/users/{user_id}/default-llm-key-usage"
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
        if isinstance(response_data, dict) and "use_main_credentials" in response_data:
            value = response_data.get("use_main_credentials")
            summary = f"use_main_credentials = {value}"
            notes = "Auth successful; returned default LLM key usage setting."
        else:
            summary = "Default LLM key usage returned"
            notes = "Auth successful; response structure unexpected."
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
        notes = "Accessible to tenant admins only."
    elif response.status_code == 404:
        label = "not found"
        summary = "User or org not found"
        notes = "Endpoint reached, but user_id or org does not exist."
    else:
        label = "error"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Unexpected response; check inputs or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint_template} | GET | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_get_default_llm_key_usage()