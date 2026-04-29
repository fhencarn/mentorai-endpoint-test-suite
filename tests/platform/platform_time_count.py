import requests
from auth import get_token

# Configuration
org_id    = "syracuse"              # Use own org_id
user_id   = "8"                     # Data_AI_Analytics user ID
course_id = "YOUR_COURSE_ID"        # e.g. course-v1:syracuse+Course+Run #Replace this!!

token   = get_token()
if not token:
    exit()

# Build request (optional date range)
url     = f"https://base.manager.ai.syr.edu/api/platform/orgs/{org_id}/courses/{course_id}/users/{user_id}/time/count"
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