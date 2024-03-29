from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
)
from ..commands import (
    ComingRecordCommand,
    ServiceCommand,
    DefaultCommand,
    MenuCommand,
    Command,
)


class CommandSelector:
    '''CommandSelector is a class that selects the appropriate command object
    to execute based on the MessageEvent or PostbackEvent type.
    '''

    # Configuration:
    # COMMAND_CALL_KEYWORD (str): The keyword that triggers the command.
    COMMAND_CALL_KEYWORD = "/"

    # COMMAND_MAPPING (dict): A mapping of keywords to command classes.
    COMMAND_MAPPING = {
        "熱門服務": ServiceCommand,
        "即將到來預約": ComingRecordCommand,
    }

    @staticmethod
    def get_command(event: MessageEvent | PostbackEvent) -> Command:
        if not isinstance(event, (MessageEvent, PostbackEvent)):
            raise TypeError("event must be MessageEvent or PostbackEvent")

        if isinstance(event, MessageEvent):
            client_command_keyword: str = event.message.text.lower()

            if client_command_keyword.strip() != CommandSelector.COMMAND_CALL_KEYWORD:
                return DefaultCommand(event)

        if isinstance(event, PostbackEvent):
            client_command_keyword = event.postback.data.lower()
        
        for key, command in CommandSelector.COMMAND_MAPPING.items():
            if key in client_command_keyword:
                return command(event)
            
        return MenuCommand(event)