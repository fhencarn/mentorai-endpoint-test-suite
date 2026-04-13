import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

# Replace with a real session UUID from sessionid endpoint
SESSION_ID = "00000000-0000-0000-0000-000000000000"


def test_get_session_by_id():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/sessions/{SESSION_ID}/"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n" + "=" * 90)
    print("TEST: Get Session by ID")
    print("=" * 90)
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)

        print(f"Status Code: {response.status_code}")

        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        except Exception:
            data = None
            print("Response Text:")
            print(response.text)

        print("\n" + "=" * 90)
        print("ENDPOINT STATUS MATRIX ROW")
        print("=" * 90)

        if response.status_code == 200:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/sessions/{session_id}/ | "
                "GET | ibl.ai docs | 200 | working | "
                "Session retrieved | Endpoint returned session data successfully. |"
            )

        elif response.status_code == 403:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/sessions/{session_id}/ | "
                "GET | ibl.ai docs | 403 | permission-restricted | "
                "Access denied | Endpoint likely restricted by role or tenant permissions. |"
            )

        elif response.status_code == 404:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/sessions/{session_id}/ | "
                "GET | ibl.ai docs | 404 | bad-request | "
                "Session not found | Provided session_id does not exist for this user. |"
            )

        elif response.status_code == 401:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/sessions/{session_id}/ | "
                "GET | ibl.ai docs | 401 | bad-request | "
                "Authentication failed | Check API key. |"
            )

        else:
            summary = response.text[:120].replace("\n", " ")
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/sessions/{{session_id}}/ | "
                f"GET | ibl.ai docs | {response.status_code} | unknown | "
                f"Unexpected response | {summary} |"
            )

    except Exception as e:
        print(
            f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/sessions/{{session_id}}/ | "
            f"GET | ibl.ai docs | ERROR | server-error | Request failed | {str(e)} |"
        )


if __name__ == "__main__":
    test_get_session_by_id()