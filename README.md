# Timesheet Automation

A Python application that automates the process of syncing time entries from Toggl to your timesheet system. The tool fetches time tracking data from Toggl, allows you to review and edit entries through a modern GUI, and then pushes them to your timesheet API.

## Features

- **Automatic Sync**: Fetches time entries from Toggl API
- **Interactive Editor**: Modern GUI popup to review and edit entries before submission
- **Smart Task Detection**: Automatically detects task types based on description keywords
- **Data Transformation**: Converts Toggl entries to your timesheet API format
- **Validation**: Review and edit entries before pushing to the API

## Requirements

- Python 3.11 or higher
- Toggl API token
- Timesheet API endpoint
- Google API key (for paraphrasing feature, optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd time_sheet_automation
```

2. Install dependencies using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following environment variables:

```env
# Toggl Configuration
toggle_url=https://api.track.toggl.com
toggle_api_key=your_toggl_api_token

# Timesheet API Configuration
time_sheet_url=https://your-timesheet-api.com/endpoint
emp_id=your_employee_id
project_id=your_project_id

# Google API (for paraphrasing, optional)
google_api_key=your_google_api_key
google_model=gemini-pro

# Timezone
time_zone=UTC
```

### Getting Your Toggl API Token

1. Log in to your Toggl account
2. Go to Profile Settings → API Token
3. Copy your API token

## Usage

Run the main script:

```bash
python main.py
```

Or using `uv`:

```bash
uv run python main.py
```

### Workflow

1. **Fetch Entries**: The script fetches time entries from Toggl for the specified date range
2. **Format Data**: Entries are automatically formatted and task types are detected based on keywords
3. **Review & Edit**: A GUI popup appears where you can:
   - Review all entries in a table format
   - Double-click any cell to edit it
   - Modify task descriptions, task types, functionality, etc.
4. **Submit**: Click "Save Changes" to push entries to your timesheet API, or "Cancel" to abort

## Project Structure

```
time_sheet_automation/
├── main.py              # Main entry point
├── config.py            # Configuration and environment variables
├── constants.py          # Enums for task types and functionality
├── toggle.py            # Toggl API integration and data transformation
├── update_api.py        # Timesheet API integration
├── popup.py             # GUI editor popup
├── paraphrase.py        # Google Gemini integration for text paraphrasing
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata and dependencies
└── README.md           # This file
```

## Task Type Detection

The application automatically detects task types based on keywords in the description:

- **Bug Fixes**: Contains "bug"
- **Meeting**: Contains "meeting"
- **Requirement**: Contains "requirement"
- **Review**: Contains "review"
- **Training/Learning**: Contains "train" or "learn"
- **New Feature**: Contains "new" or "feature"
- **Maintenance**: Default fallback

## API Parameters

Each timesheet entry includes:

- `empid`: Employee ID
- `date`: Date in YYYY-MM-DD format
- `tasktype`: Numeric task type ID
- `functionality`: Functionality name (e.g., "Order entry", "Invoice")
- `task`: Task description
- `timespent`: Time spent in HH:MM format
- `projectUID`: Project ID

## Dependencies

- `google-generativeai`: Google Gemini API for paraphrasing
- `fastapi`: Web framework (if needed for API server)
- `uvicorn`: ASGI server
- `dotenv`: Environment variable management
- `mcp`: Model Context Protocol
- `requests`: HTTP library for API calls
- `tkinter`: GUI framework (usually included with Python)

## Notes

- The date range in `toggle.py` is currently hardcoded. You may want to make this configurable.
- The application skips entries with negative duration or missing start times
- All API calls include timeout protection (10 seconds)
- The GUI popup is non-blocking and allows full editing of entries before submission

## Troubleshooting

### API Errors

If you encounter API errors:
- Check your API tokens in the `.env` file
- Verify the timesheet API endpoint URL
- Check network connectivity
- Review the error messages printed to console

### Empty Entries

If no entries appear:
- Verify the date range in `toggle.py` matches your Toggl entries
- Check that your Toggl API token has proper permissions
- Ensure entries exist in Toggl for the specified date range
