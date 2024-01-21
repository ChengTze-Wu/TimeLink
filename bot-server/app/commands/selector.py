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
    '''CommandSelector is a class that selects the appropriate command object
    to execute based on the event type and the event message.
    '''
    COMMAND_CALL_KEYWORD = "tl"
    COMMAND_MAPPING = {
        "服務": ServiceCommand,
        "記錄": RecordCommand,
        "預約": ReserveCommand
    }

    @staticmethod
    def get_command(event: MessageEvent | PostbackEvent) -> Command:
        if isinstance(event, MessageEvent):
            event_keyword = event.message.text.lower()

            if CommandSelector.COMMAND_CALL_KEYWORD not in event_keyword:
                return DefaultCommand(event)

        if isinstance(event, PostbackEvent):
            event_keyword = event.postback.data.lower()
        
        for key, command_cls in CommandSelector.COMMAND_MAPPING.items():
            if key in event_keyword:
                return command_cls(event)
            
        return MenuCommand(event)