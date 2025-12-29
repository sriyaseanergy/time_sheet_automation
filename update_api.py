import requests
from config import settings
import json


def push_to_timesheet_api(entry):
    """
    entry = Apiparameters dataclass instance
    """

    # API expects query parameters, not JSON body
    # Also, timespent should be a string according to the API validation
    params = {
        "empid": entry.empid,
        "date": entry.date,
        "tasktype": entry.tasktype,
        "functionality": entry.functionality,
        "task": entry.task,
        "timespent": entry.timespent,  # Keep as string
        "projectUID": entry.projectUID,
    }

    try:
        response = requests.put(settings.time_sheet_url, params=params, timeout=10)
        
        # Log request details for debugging
        if response.status_code != 200:
            print(f"API Error Details:")
            print(f"  URL: {settings.time_sheet_url}")
            print(f"  Params: {json.dumps(params, indent=2)}")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:500]}")  # First 500 chars
        
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        print(f"API Request Exception: {error_msg}")
        print(f"  Params: {json.dumps(params, indent=2)}")
        return None, error_msg
