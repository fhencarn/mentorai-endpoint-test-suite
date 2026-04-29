import requests
from auth import get_token

# Configuration
org_id  = "syracuse"  # Use own org_id
user_id = "8"         # Data_AI_Analytics user ID

token   = get_token()
if not token:
    exit()

# Build request
url     = f"https://base.manager.ai.syr.edu/api/ai-analytics/orgs/{org_id}/users/{user_id}/costs/model/"
headers = {"Authorization": f"Bearer {token}"}
params  = {
    "start_date": "2026-01-01",
    "end_date":   "2026-04-07"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print(f"✅ {response.status_code} working")
    print(response.json())
else:
    print(f"❌ {response.status_code}: {response.text}")