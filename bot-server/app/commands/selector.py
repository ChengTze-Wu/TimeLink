from linebot.v3.webhooks import (
    MessageEvent
)
from .record import RecordCommand
from .reserve import ReserveCommand
from .service import ServiceCommand
from .command import Command

class DefaultCommand(Command):
    async def async_execute(self):
        pass
            
class CommandSelector:
    COMMAND_CALL_KEYWORD = "tl"

    def __init__(self):
        self.strategies = {
            "服務": ServiceCommand,
            "記錄": RecordCommand,
            "預約": ReserveCommand
        }

    def get_command(self, event: MessageEvent) -> Command:
        message_text = event.message.text.lower()
        
        if self.COMMAND_CALL_KEYWORD not in message_text:
            return DefaultCommand(event)
        
        for key, command_cls in self.strategies.items():
            if key in message_text:
                return command_cls(event)
            
        return DefaultCommand(event)