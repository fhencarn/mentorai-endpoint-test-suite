import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def save_task_id(task_id, env_path=".env"):
    """
    Updates TASK_ID in .env if it exists, otherwise appends it.
    """
    if not task_id:
        return

    lines = []
    found = False

    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("TASK_ID="):
            new_lines.append(f"TASK_ID={task_id}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines[-1] += "\n"
        new_lines.append(f"TASK_ID={task_id}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def test_export_chathistory():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/export-chathistory/"

    if not API_TOKEN:
        print("❌ Missing API_TOKEN in .env")
        return False

    if not USER_ID:
        print("❌ Missing USER_ID in .env")
        return False

    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/export-chathistory/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Based on the doc screenshot, the example says "Requests: No request data."
    # So we send an empty JSON body.
    payload = {}

    print("🔍 Running Test: POST Export Chat History")
    print(f"URL: {url}")

    response = requests.post(url, headers=headers, json=payload)
    status_code = response.status_code

    try:
        data = response.json()
    except Exception:
        print("❌ Response is not JSON")
        print(response.text)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "error",
            "Non-JSON response returned",
            "Failed to parse response body"
        )
        return False

    if status_code == 200:
        task_id = data.get("task_id")

        if task_id:
            save_task_id(task_id)

            response_summary = f"Export task created; task_id returned"
            notes = f"Validated export-chat history worker endpoint and saved TASK_ID={task_id} to .env"

            print("✅ SUCCESS")
            print(f"Task ID: {task_id}")
            print("✅ TASK_ID saved to .env")

            print_matrix_row(
                "ai-mentor",
                endpoint_template,
                "POST",
                "ibl.ai docs",
                status_code,
                "working",
                response_summary,
                notes
            )
            return True

        print("⚠️ 200 received but no task_id found in response")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "review needed",
            "200 returned but task_id missing",
            "Response shape did not match expected schema"
        )
        return False

    elif status_code == 400:
        print("❌ 400 Bad Request")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "bad request",
            "Export request invalid",
            "Check request format or endpoint behavior"
        )
        return False

    elif status_code == 401:
        print("❌ 401 Unauthorized")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "auth failed",
            "Authentication failed",
            "Invalid or missing API token"
        )
        return False

    elif status_code == 403:
        print("❌ 403 Forbidden")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "permission issue",
            "Request authenticated but access denied",
            "Likely RBAC or org/user permission restriction"
        )
        return False

    elif status_code == 404:
        print("❌ 404 Not Found")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "not found",
            "Endpoint or resource not found",
            "Check org, user_id, or path"
        )
        return False

    else:
        print("❌ Unexpected Error")
        print(data)

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "POST",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Unexpected response returned",
            "Manual review recommended"
        )
        return False


if __name__ == "__main__":
    test_export_chathistory()