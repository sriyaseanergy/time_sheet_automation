import requests
from config import settings

def push_to_timesheet_api(task, updated_text):
    r = requests.post(
        settings.time_sheet_url,
        json={"id": task["id"], "description": updated_text},
    )
    return r.status_code