from http import HTTPStatus
from linebot.v3.messaging import (
    TextMessage,
)
from .command import Command
from app.messages import ViewMessage
from app.lib.fetch import APIServerFetchClient
from datetime import datetime, tzinfo


class ComingRecordCommand(Command):
    '''ComingRecordCommand is a class that handles the user record command. It
    will fetch the user's record from the API server and return it to the
    user.
    '''
    def __init__(self, event):
        super().__init__(event)
        self.fetch_client = APIServerFetchClient()

    async def async_execute(self) -> TextMessage | None:
        comming_appointment_resp = await self.__get_the_comming_appointment()
        comming_appointment_json: dict = comming_appointment_resp.json()

        if comming_appointment_resp.status_code != HTTPStatus.OK:
             return TextMessage(text=ViewMessage.NO_COMING_RECORD)

        reserved_at = comming_appointment_json.get('reserved_at')
        format_reserved_at = datetime.strptime(reserved_at, '%a, %d %b %Y %H:%M:%S %Z')
        service: dict = comming_appointment_json.get('service')
        service_name = service.get('name')
        price = service.get('price')

        return TextMessage(text=ViewMessage.MOST_COMING_RECORD.substitute(
            service_name=service_name,
            reserved_at=format_reserved_at,
            price=price
        ))
    
    async def __get_the_comming_appointment(self):
        line_user_id: str = self.event.source.user_id
        return await self.fetch_client.get(
            f'/api/users/{line_user_id}/appointments?coming=true'
        )
