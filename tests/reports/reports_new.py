import requests
from auth import get_token

# Configuration
org_id = "syracuse"  # Use own org_id

token   = get_token()
if not token:
    exit()

# Build request
# report_name should come from the list returned by reports_list.py
url     = f"https://base.manager.ai.syr.edu/api/reports/orgs/{org_id}/new"
headers = {"Authorization": f"Bearer {token}"}
body    = {
    "report_name": "YOUR_REPORT_NAME",  # Get report_name from reports_list.py output first
    "owner":       "jasidel"            # Change to your NetID
}

response = requests.post(url, headers=headers, json=body)

if response.status_code == 200:
    print(f"✅ {response.status_code} working")
    print(response.json())
else:
    print(f"❌ {response.status_code}: {response.text}")