#!/usr/bin/env python3

import os
import json
from datetime import datetime

import requests
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.iblai.app").rstrip("/")
ORG_ID = os.getenv("ORG_ID")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

# ------------------------------
# Validate required config
# ------------------------------
missing = []
if not BASE_URL:
    missing.append("BASE_URL")
if not ORG_ID:
    missing.append("ORG_ID")
if not USER_ID:
    missing.append("USER_ID")
if not API_KEY:
    missing.append("API_KEY")

if missing:
    raise ValueError(
        f"Missing required environment variable(s): {', '.join(missing)}. "
        "Check your .env file."
    )

# ------------------------------
# Headers
# ------------------------------
HEADERS = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json",
}

# ------------------------------
# Helpers
# ------------------------------
def classify_status(status_code: int) -> str:
    if status_code == 200:
        return "working"
    if status_code == 401:
        return "auth-failed"
    if status_code == 403:
        return "permission-restricted"
    if status_code == 404:
        return "not-found"
    if status_code == 400:
        return "bad-request"
    if 500 <= status_code <= 599:
        return "server-error"
    return "unknown"

def summarize_response(response: requests.Response) -> str:
    try:
        data = response.json()
        if isinstance(data, dict):
            if "results" in data and isinstance(data["results"], list):
                return f"{len(data['results'])} mentor(s) returned"
            return f"JSON returned with keys: {list(data.keys())[:6]}"
        return "JSON response returned"
    except Exception:
        text = response.text.strip().replace("\n", " ")
        return text[:160] if text else "No response body"

# ------------------------------
# Main test
# ------------------------------
def test_list_mentors():
    endpoint = f"/api/ai-mentor/orgs/{ORG_ID}/users/{USER_ID}/"
    url = f"{BASE_URL}{endpoint}"

    print(f"\n[TEST] GET {url}")
    print(f"[INFO] ORG_ID={ORG_ID}")
    print(f"[INFO] USER_ID={USER_ID}")
    print(f"[INFO] API_KEY loaded={'yes' if API_KEY else 'no'}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
    except requests.RequestException as exc:
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint_template": "/api/ai-mentor/orgs/{org}/users/{user_id}/",
            "resolved_endpoint": endpoint,
            "method": "GET",
            "status_code": None,
            "label": "request-failed",
            "summary": str(exc),
        }
        print(json.dumps(result, indent=2))
        return result

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint_template": "/api/ai-mentor/orgs/{org}/users/{user_id}/",
        "resolved_endpoint": endpoint,
        "method": "GET",
        "status_code": response.status_code,
        "label": classify_status(response.status_code),
        "summary": summarize_response(response),
    }

    print(json.dumps(result, indent=2))

    # Optional preview of first few mentors
    try:
        data = response.json()
        results = data.get("results", [])
        if isinstance(results, list) and results:
            print("\n[MENTOR PREVIEW]")
            for mentor in results[:3]:
                print(
                    {
                        "name": mentor.get("name"),
                        "unique_id": mentor.get("unique_id"),
                        "slug": mentor.get("slug"),
                    }
                )
    except Exception:
        pass

    return result


if __name__ == "__main__":
    test_list_mentors()