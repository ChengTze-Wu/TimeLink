from httpx import post
from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
)
from .record import RecordCommand
from .reserve import ReserveCommand
from .service import ServiceCommand
from .default import DefaultCommand
from .menu import MenuCommand
from .command import Command


class CommandSelector:
    COMMAND_CALL_KEYWORD = "tl"

    def __init__(self):
        self.strategies = {
            "服務": ServiceCommand,
            "記錄": RecordCommand,
            "預約": ReserveCommand
        }

    def get_command(self, event: MessageEvent | PostbackEvent) -> Command:
        if isinstance(event, MessageEvent):
            event_keyword = event.message.text.lower()

            if self.COMMAND_CALL_KEYWORD not in event_keyword:
                return DefaultCommand(event)

        if isinstance(event, PostbackEvent):
            event_keyword = event.postback.data.lower()
        
        for key, command_cls in self.strategies.items():
            if key in event_keyword:
                return command_cls(event)
            
        return MenuCommand(event)