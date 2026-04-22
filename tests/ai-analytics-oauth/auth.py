import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID     = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL     = "https://base.manager.ai.syr.edu/oauth/token/"

def get_token():
    response = requests.post(TOKEN_URL, data={
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type":    "client_credentials",
        "resource":      "https://base.manager.ai.domain.com"
    })

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Token retrieved")
        return token
    else:
        print(f"❌ Failed to get token: {response.status_code}: {response.text}")
        return None