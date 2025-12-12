import requests
from config import settings


def push_to_timesheet_api(entry):
    """
    entry = Apiparameters dataclass instance
    """

    payload = {
        "empid": entry.empid,
        "date": entry.date,
        "tasktype": entry.tasktype,
        "functionality": entry.functionality,
        "task": entry.task,
        "timespent": entry.timespent,
        "projectUID": entry.projectUID,
    }

    response = requests.put(settings.time_sheet_url, json=payload, timeout=10)

    return response.status_code, response.text
