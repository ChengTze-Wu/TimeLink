import os
import httpx
from .command import Command

API_SERVER_HOST = os.getenv("API_SERVER_HOST", None)

class RecordCommand(Command):
    async def async_execute(self):
        user_id = self.event.source.user_id
        async with httpx.AsyncClient() as client:
            headers = {'user-agent': 'TimeLink-Line-Bot/0.0.1'}
            user_resp = await client.get(f'{API_SERVER_HOST}/api/users/line/{user_id}', timeout=2, headers=headers)
        user_json: dict = user_resp.json()
        appointments: list = user_json.get("appointments")
        return f"你共有 {len(appointments)} 筆預約"