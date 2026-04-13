import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")


def test_get_tenant_llm():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/settings/tenant-llm/"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n" + "=" * 90)
    print("TEST: Get Tenant LLM")
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
            count = len(data) if isinstance(data, list) else data.get("count", "unknown") if isinstance(data, dict) else "unknown"
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/settings/tenant-llm/ | "
                f"GET | ibl.ai docs | 200 | working | "
                f"Tenant LLM models retrieved (count={count}) | "
                f"Endpoint returned available LLM models for the tenant successfully. |"
            )

        elif response.status_code == 403:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/settings/tenant-llm/ | "
                "GET | ibl.ai docs | 403 | permission-restricted | "
                "Access denied | Endpoint likely restricted by role or tenant permissions. |"
            )

        elif response.status_code == 404:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/settings/tenant-llm/ | "
                "GET | ibl.ai docs | 404 | undocumented | "
                "Endpoint not found | Route may be unavailable or not deployed. |"
            )

        elif response.status_code == 401:
            print(
                "| ai-mentor | /api/ai-mentor/orgs/{org}/users/{user_id}/settings/tenant-llm/ | "
                "GET | ibl.ai docs | 401 | bad-request | "
                "Authentication failed | Check API key. |"
            )

        else:
            summary = response.text[:120].replace("\n", " ")
            print(
                f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/settings/tenant-llm/ | "
                f"GET | ibl.ai docs | {response.status_code} | unknown | "
                f"Unexpected response | {summary} |"
            )

    except Exception as e:
        print(
            f"| ai-mentor | /api/ai-mentor/orgs/{{org}}/users/{{user_id}}/settings/tenant-llm/ | "
            f"GET | ibl.ai docs | ERROR | server-error | "
            f"Request failed | {str(e)} |"
        )


if __name__ == "__main__":
    test_get_tenant_llm()