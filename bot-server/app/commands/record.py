from http import HTTPStatus
from linebot.v3.messaging import (
    TextMessage,
)
from .command import Command
from app.messages import ViewMessage
from app.utils.fetch import APIServerFetchClient
from datetime import datetime, tzinfo


class ComingRecordCommand(Command):
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
        coming_appointment_message = await self.__format_coming_appointment(user_json)

        return TextMessage(text=coming_appointment_message)
    
    async def __get_user(self):
        line_user_id: str = self.event.source.user_id
        return await self.fetch_client.get(f'/api/users/{line_user_id}')
    
    async def __get_service(self, service_id: str):
        return await self.fetch_client.get(f'/api/services/{service_id}')
    
    async def __format_coming_appointment(self, user_json: dict):
        appointments: list[dict] = user_json.get("appointments")
        
        most_coming_appointment = None
        now = datetime.now()
        for appointment in appointments:
            reserved_at = datetime.strptime(appointment.get("reserved_at"), "%a, %d %b %Y %H:%M:%S %Z")
            if reserved_at >= now:
                if not most_coming_appointment:
                    most_coming_appointment = appointment
                most_coming_reserved_at = datetime.strptime(most_coming_appointment.get("reserved_at"), "%a, %d %b %Y %H:%M:%S %Z")
                if reserved_at < most_coming_reserved_at:
                    most_coming_appointment = appointment

        if not most_coming_appointment:
            return ViewMessage.NO_COMING_RECORD
        
        service_response = await self.__get_service(most_coming_appointment.get("service_id"))
        service: dict = service_response.json()
        format_reserved_at = datetime.strptime(most_coming_appointment.get("reserved_at"), "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d %H:%M:%S")

        return ViewMessage.MOST_COMING_RECORD.substitute(service_name=service.get("name"),
                                                         reserved_at=format_reserved_at,
                                                         price=service.get("price"))
    
    async def __handle_response(self, response) -> ViewMessage | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return ViewMessage.USER_NOT_LINKED
        
        if response.status_code == HTTPStatus.OK:
            return response

        return None


class AllRecordCommand(Command):
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
