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


def test_get_metadata():
    endpoint_template = "/api/ai-mentor/orgs/{org}/users/{user_id}/metadata"
    url = f"{BASE_URL}{endpoint_template.format(org=ORG, user_id=USER_ID)}"

    headers = {
        "Authorization": f"Api-Token {API_TOKEN}"
    }

    print("🔍 Running Test: GET Metadata")
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            try:
                data = response.json()

                # Expected structure (if populated)
                metadata = data.get("metadata")
                mentor = data.get("mentor")

                print("✅ SUCCESS (JSON response)")
                print(f"Metadata keys: {list(metadata.keys()) if metadata else 'None'}")

                print_matrix_row(
                    "ai-mentor",
                    endpoint_template,
                    "GET",
                    "ibl.ai docs",
                    status_code,
                    "working",
                    "metadata object returned",
                    f"mentor={mentor}"
                )

            except ValueError:
                # Handles "No Body" case (like your screenshot)
                print("⚠️ SUCCESS (No JSON body returned)")

                print_matrix_row(
                    "ai-mentor",
                    endpoint_template,
                    "GET",
                    "ibl.ai docs",
                    status_code,
                    "review needed",
                    "no response body returned",
                    "Docs say metadata object expected"
                )

        else:
            print(f"❌ FAILED: Status {status_code}")
            print(response.text)

            print_matrix_row(
                "ai-mentor",
                endpoint_template,
                "GET",
                "ibl.ai docs",
                status_code,
                "failed",
                "request failed",
                response.text[:100]
            )

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

        print_matrix_row(
            "ai-mentor",
            endpoint_template,
            "GET",
            "ibl.ai docs",
            "N/A",
            "error",
            "exception occurred",
            str(e)
        )


if __name__ == "__main__":
    test_get_metadata()