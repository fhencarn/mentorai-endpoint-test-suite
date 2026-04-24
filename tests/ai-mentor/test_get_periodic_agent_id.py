"""
Endpoint test for:
GET /api/ai-mentor/orgs/{org}/users/{user_id}/periodic-agents/{id}/

Matrix fields:
- endpoint_name
- method
- path
- test_id_used
- status_code
- result
- notes
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def classify_result(status_code: int) -> str:
    if status_code == 200:
        return "Working"
    if status_code == 403:
        return "Permission Restricted"
    if status_code == 404:
        return "Not Found / ID Invalid"
    if status_code == 401:
        return "Auth Failed"
    if 500 <= status_code <= 599:
        return "Server Error"
    return "Needs Review"


def build_notes(status_code: int) -> str:
    if status_code == 200:
        return "Endpoint reachable and returned periodic agent record."
    if status_code == 403:
        return "Endpoint exists but token likely lacks platform admin or tenant admin access."
    if status_code == 404:
        return "Endpoint exists but requested periodic agent ID was not found."
    if status_code == 401:
        return "API token missing, invalid, or expired."
    if 500 <= status_code <= 599:
        return "Server-side error returned by endpoint."
    return "Unexpected response; review raw output."


def test_get_periodic_agent():
    base_url = os.getenv("BASE_URL", "https://base.manager.iblai.app")
    org = os.getenv("ORG_ID", "syracuse")
    user_id = os.getenv("USER_ID")
    api_token = os.getenv("API_KEY")
    periodic_agent_id = os.getenv("PERIODIC_AGENT_ID", "1")

    if not user_id:
        raise ValueError("Missing USER_ID in environment.")
    if not api_token:
        raise ValueError("Missing API_TOKEN in environment.")

    path = f"/api/ai-mentor/orgs/{org}/users/{user_id}/periodic-agents/{periodic_agent_id}/"
    url = f"{base_url}{path}"
    headers = {
        "Authorization": f"Api-Token {api_token}",
        "Content-Type": "application/json",
    }

    endpoint_name = "Get Periodic Agent by ID"
    method = "GET"

    print("\n" + "=" * 90)
    print(f"TEST: {endpoint_name}")
    print("=" * 90)
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        status_code = response.status_code
        result = classify_result(status_code)
        notes = build_notes(status_code)

        print(f"Status Code: {status_code}")

        try:
            body = response.json()
            print("Response JSON:")
            print(body)
        except ValueError:
            body = response.text
            print("Response Text:")
            print(body)

        print("\n" + "-" * 90)
        print("ENDPOINT STATUS MATRIX ROW")
        print("-" * 90)
        print(
            f"{endpoint_name} | {method} | {path} | {periodic_agent_id} | "
            f"{status_code} | {result} | {notes}"
        )

    except requests.RequestException as e:
        print("\nERROR: Request failed.")
        print(str(e))

        print("\n" + "-" * 90)
        print("ENDPOINT STATUS MATRIX ROW")
        print("-" * 90)
        print(
            f"Get Periodic Agent by ID | GET | {path} | {periodic_agent_id} | "
            f"REQUEST FAILED | Needs Review | {str(e)}"
        )


if __name__ == "__main__":
    test_get_periodic_agent()