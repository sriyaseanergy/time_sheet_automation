import requests
from config import settings

API_TOKEN = settings.toggle_api
base_url = "https://api.track.toggl.com/api/v9"

def fetch_toggl_tasks(api_token: str):
    resp = requests.get(
        settings.toggle_url,
        auth=(api_token, "api_token")
    )
    resp.raise_for_status()
    return resp.json()
