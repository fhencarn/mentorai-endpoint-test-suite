import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_KEY")


def test_get_pin_message():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/pin-message/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("\n" + "=" * 90)
    print("TEST: Get Pin Message")
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

        # =========================
        # MATRIX OUTPUT
        # =========================

        if response.status_code == 200:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/pin-message/ | "
                f"GET | ibl.ai docs | 200 | working | "
                f"Pinned message retrieved | Endpoint returned expected object (id, session_id, etc.). |"
            )

        elif response.status_code == 403:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/pin-message/ | "
                f"GET | ibl.ai docs | 403 | permission-restricted | "
                f"Access denied | Unexpected if docs are correct (should be accessible to students). May indicate tenant-specific permission issue. |"
            )

        elif response.status_code == 401:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/pin-message/ | "
                f"GET | ibl.ai docs | 401 | bad-request | "
                f"Authentication failed | Check API token. |"
            )

        elif response.status_code == 404:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/pin-message/ | "
                f"GET | ibl.ai docs | 404 | undocumented | "
                f"Endpoint not found | Route may be incorrect or not deployed. |"
            )

        else:
            summary = response.text[:120].replace("\n", " ")

            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/pin-message/ | "
                f"GET | ibl.ai docs | {response.status_code} | unknown | "
                f"Unexpected response | {summary} |"
            )

    except Exception as e:
        print("Request failed:", str(e))

        print(
            f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/pin-message/ | "
            f"GET | ibl.ai docs | ERROR | server-error | "
            f"Request failed | {str(e)} |"
        )


if __name__ == "__main__":
    test_get_pin_message()
