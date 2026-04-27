import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://base.manager.ai.syr.edu"
API_KEY = os.getenv("API_KEY")

ORG = "syracuse"

CREDENTIAL_NAME = "endpoint-test-openai"
CREDENTIAL_VALUE = {
    "key": "sk-test-placeholder-updated"
}
PLATFORM = "main"


def test_patch_ai_account_credential():
    endpoint_template = "/api/ai-account/orgs/{org}/credential/"
    endpoint = endpoint_template.format(org=ORG)
    url = f"{BASE_URL}{endpoint}"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "name": CREDENTIAL_NAME,
        "value": CREDENTIAL_VALUE,
        "platform": PLATFORM,
    }

    response = requests.patch(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)

    try:
        response_data = response.json()
        print("Response JSON:", response_data)
    except Exception:
        response_data = response.text
        print("Response Text:", response_data[:300])

    if response.status_code == 200:
        label = "working"
        summary = "LLM credential updated"
        notes = "Auth successful; updated tenant LLM credential."
    elif response.status_code == 400:
        label = "bad request"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Request reached endpoint, but payload may be invalid or credential name may already exist."
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
        summary = "Credential or org not found"
        notes = "Endpoint reached, but tenant org or credential name was not found."
    else:
        label = "error"
        summary = str(response_data)[:200].replace("\n", " ")
        notes = "Unexpected response; check payload, org, permissions, or server behavior."

    print("\n--- Endpoint Matrix Row ---")
    print(
        f"| ai-account | {endpoint_template} | PATCH | ibl.ai docs | "
        f"{response.status_code} | {label} | {summary} | {notes} |"
    )


if __name__ == "__main__":
    test_patch_ai_account_credential()