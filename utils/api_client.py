from __future__ import annotations

from typing import Any

import requests

from utils.config import API_KEY


def build_headers() -> dict[str, str]:
    return {
        "Authorization": f"Api-Token {API_KEY}",
        "Content-Type": "application/json",
    }


def classify_status(status_code: int) -> str:
    if status_code in (200, 201, 202, 204):
        return "working"
    if status_code == 400:
        return "bad-request"
    if status_code == 401:
        return "permission-restricted"
    if status_code == 403:
        return "syracuse-permission-issue"
    if status_code == 404:
        return "undocumented"
    if 500 <= status_code <= 599:
        return "server-error"
    return "unknown"


def summarize_response(response: requests.Response) -> str:
    try:
        data: Any = response.json()
        if isinstance(data, dict):
            keys = list(data.keys())[:8]
            return f"JSON response with keys: {keys}"
        if isinstance(data, list):
            return f"JSON list with {len(data)} items"
        return f"JSON type: {type(data).__name__}"
    except Exception:
        text = response.text.strip().replace("\n", " ")
        return text[:200] if text else "No response body"
