import requests
from auth import get_token

# Configuration
org_id  = "syracuse"  # Use own org_id
user_id = "8"         # Data_AI_Analytics user ID

token   = get_token()
if not token:
    exit()

# Build request
url     = f"https://base.manager.ai.syr.edu/api/ai-analytics/orgs/{org_id}/users/{user_id}/sentiment-count/"
headers = {"Authorization": f"Bearer {token}"}
params  = {"period": "7d"}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print(f"✅ {response.status_code} working")
    print(response.json())
else:
    print(f"❌ {response.status_code}: {response.text}")