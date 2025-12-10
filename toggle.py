import requests
from config import settings
from datetime import datetime, timedelta
from dataclasses import dataclass
from constants import Tasktype

API_TOKEN = settings.toggle_api

date = datetime.now()
yesterday = date - timedelta(days=1)
print(yesterday)


def fetch_toggl_tasks(api_token: str):
    url = "https://api.track.toggl.com/api/v9/me/time_entries?start_date=2025-12-09&end_date=2025-12-10"
    resp = requests.get(url, auth=(api_token, "api_token"))
    resp.raise_for_status()
    result = resp.json()
    print(result)
    return result


fetch_toggl_tasks(api_token=API_TOKEN)


def detect_task_type(description: str) -> int:
    desc = description.lower()

    if "bug" in desc:
        return Tasktype.Development_Bug_Fixes.value
    if "meeting" in desc:
        return Tasktype.Meeting_Internal.value
    if "requirement" in desc:
        return Tasktype.Requirement.value
    if "review" in desc:
        return Tasktype.Review_Code_Design.value
    if "train" in desc or "learn" in desc:
        return Tasktype.Training_learning.value
    if "new" in desc or "feature" in desc:
        return Tasktype.Development_New_Feature.value

    # fallback
    return Tasktype.Development_Maintanace.value


def to_hhmm(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


def extract_date(start_timestamp: str) -> str:
    dt = datetime.fromisoformat(start_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d")


def create_response_body_from_toggl_taks(results):
    response_list = []

    for entry in results:
        description = entry.get("description", "")
        duration_seconds = entry.get("duration", 0)
        start = entry.get("start")

        payload = Apiparameters(
            empid=settings.emp_id,
            date=extract_date(start),
            tasktype=detect_task_type(description),
            functionality=description,
            task=description,
            timespent=to_hhmm(duration_seconds),
            projectUID=settings.project_id,
        )

        response_list.append(payload)

    return response_list


@dataclass
class Apiparameters:
    empid: int = 0
    date: str = ""
    tasktype: str = ""
    functionality: str = ""
    task: str = ""
    timespent: str = ""
    projectUID: str = ""
