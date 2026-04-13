import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

TASK_ID = 1  # replace with a real task ID if you have one


def test_get_task_status():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/tasks/{TASK_ID}"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n" + "=" * 90)
    print("TEST: Get Task Status")
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
            task_status = data.get("task", "unknown") if isinstance(data, dict) else "unknown"
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/tasks/{{task_id}} | "
                f"GET | ibl.ai docs | 200 | working | "
                f"Task status retrieved ({task_status}) | "
                f"Endpoint returned worker task status successfully. |"
            )

        elif response.status_code == 403:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/tasks/{task_id} | "
                "GET | ibl.ai docs | 403 | permission-restricted | "
                "Access denied | Endpoint likely restricted by role or tenant permissions. |"
            )

        elif response.status_code == 404:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/tasks/{task_id} | "
                "GET | ibl.ai docs | 404 | bad-request | "
                "Task not found | Provided task_id does not exist for this user. |"
            )

        elif response.status_code == 401:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/tasks/{task_id} | "
                "GET | ibl.ai docs | 401 | bad-request | "
                "Authentication failed | Check API key. |"
            )

        else:
            summary = response.text[:120].replace("\n", " ")
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/tasks/{{task_id}} | "
                f"GET | ibl.ai docs | {response.status_code} | unknown | "
                f"Unexpected response | {summary} |"
            )

    except Exception as e:
        print(
            f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/tasks/{{task_id}} | "
            f"GET | ibl.ai docs | ERROR | server-error | "
            f"Request failed | {str(e)} |"
        )


if __name__ == "__main__":
    test_get_task_status()