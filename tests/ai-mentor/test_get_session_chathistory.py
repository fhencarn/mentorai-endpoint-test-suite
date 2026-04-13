import requests, json, os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
ORG = os.getenv("ORG")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

SESSION_ID = "00000000-0000-0000-0000-000000000000"


def test_get_session_chathistory():
    url = f"{BASE_URL}/api/ai-mentor/orgs/{ORG}/users/{USER_ID}/sessions/{SESSION_ID}/"

    headers = {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n" + "="*90)
    print("TEST: Download Session Chat History")
    print("="*90)
    print(f"URL: {url}")

    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {r.status_code}")

        try:
            data = r.json()
            print(json.dumps(data, indent=2))
        except:
            print(r.text)

        print("\n" + "="*90)
        print("ENDPOINT STATUS MATRIX ROW")
        print("="*90)

        if r.status_code == 200:
            print("| ai-mentor | /sessions/{session_id}/ | GET | ibl.ai docs | 200 | working | Chat history downloaded | Endpoint returned session history successfully. |")
        elif r.status_code == 403:
            print("| ai-mentor | /sessions/{session_id}/ | GET | ibl.ai docs | 403 | permission-restricted | Access denied | Restricted by role or tenant permissions. |")
        elif r.status_code == 404:
            print("| ai-mentor | /sessions/{session_id}/ | GET | ibl.ai docs | 404 | bad-request | Session not found | Invalid session_id provided. |")
        else:
            print(f"| ai-mentor | /sessions/{{session_id}}/ | GET | ibl.ai docs | {r.status_code} | unknown | Unexpected response | {r.text[:100]} |")

    except Exception as e:
        print(f"| ai-mentor | /sessions/{{session_id}}/ | GET | ibl.ai docs | ERROR | server-error | Request failed | {str(e)} |")


if __name__ == "__main__":
    test_get_session_chathistory()