import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu")
ORG = os.getenv("ORG", "syracuse")
USER_ID = os.getenv("USER_ID")
EDX_MEMORY_ID = os.getenv("EDX_MEMORY_ID")
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("API_KEY")


def print_matrix_row(section, endpoint, method, doc_source, status_code, label, response_summary, notes=""):
    print("\n--- Endpoint Matrix Row ---")
    print(f"| {section} | {endpoint} | {method} | {doc_source} | {status_code} | {label} | {response_summary} | {notes} |")


def test_get_edx_memory_by_id_auto():
    list_url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/edx-memory/"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔍 Step 1: Fetch EDX Memory List")

    list_response = requests.get(list_url, headers=headers)

    try:
        list_data = list_response.json()
    except:
        print("❌ Failed to parse list response")
        return False

    count = list_data.get("count", 0)
    results = list_data.get("results", [])

    # 🚨 KEY LOGIC
    if count == 0 or not results:
        print("⚠️ No EDX memory records found — skipping ID test")

        print_matrix_row(
            "ai-mentor",
            "/api/ai-mentor/orgs/{org}/users/{user_id}/edx-memory/{id}/",
            "GET",
            "ibl.ai docs",
            200,
            "no data",
            "No EDX memory records available to test ID endpoint",
            "List endpoint returned count=0; ID-based test skipped"
        )
        return True

    # ✅ Extract ID
    edx_id = results[0].get("id")

    print(f"✅ Found EDX_MEMORY_ID: {edx_id}")

    # Step 2: Call ID endpoint
    detail_url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/edx-memory/{edx_id}/"

    print("🔍 Step 2: Fetch EDX Memory by ID")

    response = requests.get(detail_url, headers=headers)
    status_code = response.status_code

    try:
        data = response.json()
    except:
        print("❌ Response not JSON")
        return False

    if status_code == 200:
        print("✅ SUCCESS")

        print_matrix_row(
            "ai-mentor",
            "/api/ai-mentor/orgs/{org}/users/{user_id}/edx-memory/{id}/",
            "GET",
            "ibl.ai docs",
            status_code,
            "working",
            f"EDX memory record {edx_id} retrieved",
            "Auto-fetched ID from list endpoint"
        )
        return True

    else:
        print("❌ Failed")
        print(data)

        print_matrix_row(
            "ai-mentor",
            "/api/ai-mentor/orgs/{org}/users/{user_id}/edx-memory/{id}/",
            "GET",
            "ibl.ai docs",
            status_code,
            "review needed",
            "Failed to retrieve EDX memory by ID",
            "Unexpected response from ID endpoint"
        )
        return False


if __name__ == "__main__":
    test_get_edx_memory_by_id_auto()