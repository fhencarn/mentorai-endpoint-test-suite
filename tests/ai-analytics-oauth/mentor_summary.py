import requests
from auth import get_token

# Configuration
org_id  = "syracuse"  # Use own org_id
user_id = "8"         # Data_AI_Analytics user ID

token   = get_token()
if not token:
    exit()

# Build request (no date params required)
url     = f"https://base.manager.ai.syr.edu/api/ai-analytics/orgs/{org_id}/users/{user_id}/mentor-summary/"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(f"✅ {response.status_code} working")
    print(response.json())
else:
    print(f"❌ {response.status_code}: {response.text}")