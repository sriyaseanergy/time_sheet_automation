from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    google_api_key = os.getenv("google_api_key")
    toggle_url = os.getenv("toggle_url")
    toggle_api = os.getenv("toggle_api_key")
    time_sheet_url = os.getenv("time_sheet_url")
    time_zone = os.getenv("time_zone")
    google_model = os.getenv("google_model")
    emp_id = os.getenv("emp_id")
    project_id = os.getenv("project_id")


try:
    settings = Settings()
except Exception as e:
    raise EnvironmentError(f"Environment not configured correctly: {e}")
