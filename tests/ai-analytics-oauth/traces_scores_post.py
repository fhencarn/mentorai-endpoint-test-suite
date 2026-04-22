import requests
from auth import get_token

# Configuration
org_id  = "syracuse"  # Use own org_id
user_id = "8"         # Data_AI_Analytics user ID

token   = get_token()
if not token:
    exit()

# Build request
url     = f"https://base.manager.ai.syr.edu/api/ai-analytics/orgs/{org_id}/users/{user_id}/traces/scores/"
headers = {"Authorization": f"Bearer {token}"}

# Dummy payload to test the endpoint
body = {
    "id":            "test-id",
    "traceId":       "test-trace-id",
    "name":          "test-score",
    "value":         1,
    "observationId": "test-observation-id",
    "comment":       "test comment"
}

response = requests.post(url, headers=headers, json=body)

if response.status_code == 200:
    print(f"✅ {response.status_code} working")
    print(response.json())
else:
    print(f"❌ {response.status_code}: {response.text}")