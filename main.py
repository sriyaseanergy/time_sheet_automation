from toggle import fetch_toggl_tasks, create_response_body_from_toggl_taks
from update_api import push_to_timesheet_api
from popup import show_edit_popup
from config import settings


def run_timesheet_sync():
    raw_entries = fetch_toggl_tasks(settings.toggle_api)
    formatted_entries = create_response_body_from_toggl_taks(raw_entries)

    edited_entries = show_edit_popup(formatted_entries)

    if not edited_entries:
        print("Cancelled. No API calls made.")
        return

    for entry in edited_entries:
        status, msg = push_to_timesheet_api(entry)
        print(f"[{entry.date}] → {entry.task} → {status} → {msg}")


if __name__ == "__main__":
    run_timesheet_sync()
