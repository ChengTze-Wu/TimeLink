from http import HTTPStatus
from .command import Command
from ..utils.fetch import APIServerFetchClient
from ..messages import ViewMessage


class RecordCommand(Command):
    def __init__(self, event):
        super().__init__(event)
        self.fetch = APIServerFetchClient()

    async def async_execute(self):
        line_user_id: str = self.event.source.user_id
        user_resp = await self.fetch.get(f'/api/users/{line_user_id}')

        if user_resp.status_code == HTTPStatus.NOT_FOUND:
            return ViewMessage.USER_NOT_LINKED
        
        if user_resp.status_code == HTTPStatus.FORBIDDEN:
            return
        
        user_json: dict = user_resp.json()
        appointments: list = user_json.get("appointments")

        if appointments is None:
            return ViewMessage.NO_RECORD

        return ViewMessage.RECORD.substitute(
            count=len(appointments),
            appointments="\n".join([f"{appointment.get('reserved_at')}" for appointment in appointments])
        )