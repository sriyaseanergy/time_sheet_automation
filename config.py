from dotenv import load_dotenv
import os

load_dotenv()
class Settings:
    claude_api_key = os.getenv("ANTHROPIC_API_KEY")
    toggle_url = os.getenv("toggle_url")
    toggle_api = os.getenv("toggle_api_key")
    time_sheet_url = os.getenv("time_sheet_url")
try:
    settings = Settings()
except Exception as e:
    raise EnvironmentError(f"Environment not configured correctly: {e}")
