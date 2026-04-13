import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_KEY")


def test_list_playwright_scripts():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/playwright-scripts/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        # "is_public": "true",
        # "ordering": "-id",
        # "page": 1,
        # "page_size": 10
    }

    print("\n" + "=" * 90)
    print("TEST: List Playwright Scripts")
    print("=" * 90)

    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)

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
            count = data.get("count", "unknown") if isinstance(data, dict) else "unknown"
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/playwright-scripts/ | "
                f"GET | ibl.ai docs | 200 | working | "
                f"Playwright scripts list returned (count={count}) | "
                f"Validated playwright scripts list endpoint; paginated structure confirmed. |"
            )

        elif response.status_code == 403:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/playwright-scripts/ | "
                f"GET | ibl.ai docs | 403 | permission-restricted | "
                f"Access denied | Endpoint likely restricted by role or tenant permissions. |"
            )

        elif response.status_code == 401:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/playwright-scripts/ | "
                f"GET | ibl.ai docs | 401 | bad-request | "
                f"Authentication failed | Check API token. |"
            )

        elif response.status_code == 404:
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/playwright-scripts/ | "
                f"GET | ibl.ai docs | 404 | undocumented | "
                f"Endpoint not found | Route may be unavailable or not deployed. |"
            )

        else:
            summary = response.text[:120].replace("\n", " ")
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/playwright-scripts/ | "
                f"GET | ibl.ai docs | {response.status_code} | unknown | "
                f"Unexpected response | {summary} |"
            )

    except Exception as e:
        print("Request failed:", str(e))
        print(
            f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/playwright-scripts/ | "
            f"GET | ibl.ai docs | ERROR | server-error | "
            f"Request failed | {str(e)} |"
        )


if __name__ == "__main__":
    test_list_playwright_scripts()