import requests
from auth import get_token

# Configuration
org_id = "syracuse"  # Use own org_id

token   = get_token()
if not token:
    exit()

# Build request (no user_id needed for reports)
url     = f"https://base.manager.ai.syr.edu/api/reports/orgs/{org_id}/"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(f"✅ {response.status_code} working")
    print(response.json())
else:
    print(f"❌ {response.status_code}: {response.text}")