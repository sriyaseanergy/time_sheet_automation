from anthropic import Anthropic

from config import settings

api_key = settings.claude_api_key

client = Anthropic(api_key=settings.claude_api_key)
def rephrase_task_with_claude(description: str) -> str:
    prompt = f"Rephrase this task to be concise, action-driven, and well-phrased:\n\nTask: {description} to add in the time sheet"
    response = client.messages.create(
        model="claude-4-sonnet-20241022",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text.strip()