from http import HTTPStatus
from linebot.v3.messaging import (
    TextMessage,
)
from .command import Command
from app.messages import ViewMessage
from app.utils.fetch import APIServerFetchClient


class RecordCommand(Command):
    '''RecordCommand is a class that handles the user record command. It
    will fetch the user's record from the API server and return it to the
    user.
    '''
    def __init__(self, event):
        super().__init__(event)
        self.fetch_client = APIServerFetchClient()

    async def async_execute(self) -> TextMessage | None:
        user_response = await self.__get_user()
        handled_response = await self.__handle_response(user_response)

        if not handled_response:
            return None

        if isinstance(handled_response, ViewMessage):
            return TextMessage(text=handled_response)
        
        user_json: dict = user_response.json()
        appointment_message = await self.__format_appointments(user_json)

        return TextMessage(text=appointment_message)
    
    async def __get_user(self):
        line_user_id: str = self.event.source.user_id
        return await self.fetch_client.get(f'/api/users/{line_user_id}')
    
    async def __format_appointments(self, user_json: dict):
        appointments = user_json.get("appointments")

        if not appointments:
            return ViewMessage.NO_RECORD

        formatted_appointments = "\n".join(
            f"{appointment['reserved_at']}" for appointment in appointments
        )

        return ViewMessage.RECORD.substitute(count=len(appointments),
                                             appointments=formatted_appointments)
    
    async def __handle_response(self, response) -> ViewMessage | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return ViewMessage.USER_NOT_LINKED
        
        if response.status_code == HTTPStatus.OK:
            return response

        return None