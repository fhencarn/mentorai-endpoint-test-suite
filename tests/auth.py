import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://base.manager.ai.syr.edu").rstrip("/")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_access_token() -> str:
    response = requests.post(
        f"{BASE_URL}/oauth/token/",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
            "resource": "https://base.manager.ai.domain.com",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def get_auth_headers() -> dict:
    token = get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }