import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")


def test_get_recommend_courses_block():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/recommend-courses-block/"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n" + "=" * 90)
    print("TEST: Recommend Course Blocks")
    print("=" * 90)

    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)

        print(f"Status Code: {response.status_code}")

        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except:
            data = None
            print(response.text)

        print("\n" + "=" * 90)
        print("ENDPOINT STATUS MATRIX ROW")
        print("=" * 90)

        if response.status_code == 200:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/recommend-courses-block/ | "
                "GET | ibl.ai docs | 200 | working | "
                "Recommended course blocks retrieved | Endpoint returned structured course block data. |"
            )

        elif response.status_code == 403:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/recommend-courses-block/ | "
                "GET | ibl.ai docs | 403 | permission-restricted | "
                "Access denied | Endpoint likely restricted by role or tenant permissions. |"
            )

        else:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/recommend-courses-block/ | "
                f"GET | ibl.ai docs | {response.status_code} | unknown | Unexpected response | |"
            )

    except Exception as e:
        print(
            f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/recommend-courses-block/ | "
            f"GET | ibl.ai docs | ERROR | server-error | Request failed | {str(e)} |"
        )


if __name__ == "__main__":
    test_get_recommend_courses_block()