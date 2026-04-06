import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "")
ORG_ID = os.getenv("ORG_ID", "")
USER_ID = os.getenv("USER_ID", "")
MENTOR_ID = os.getenv("MENTOR_ID", "")
DOCUMENT_ID = os.getenv("DOCUMENT_ID", "")


def missing_required_env() -> list[str]:
    required = {
        "API_KEY": API_KEY,
        "BASE_URL": BASE_URL,
        "ORG_ID": ORG_ID,
        "USER_ID": USER_ID,
    }
    return [key for key, value in required.items() if not value]
