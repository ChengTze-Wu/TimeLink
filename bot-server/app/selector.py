from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
)
from .commands import (
    RecordCommand,
    AppointmentCommand,
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
        "服務": ServiceCommand,
        "記錄": RecordCommand,
        "預約": AppointmentCommand
    }

    @staticmethod
    def get_command(event: MessageEvent | PostbackEvent) -> Command:
        if not isinstance(event, (MessageEvent, PostbackEvent)):
            raise TypeError("event must be MessageEvent or PostbackEvent")

        if isinstance(event, MessageEvent):
            client_command_keyword = event.message.text.lower()

            if client_command_keyword != CommandSelector.COMMAND_CALL_KEYWORD:
                return DefaultCommand(event)

        if isinstance(event, PostbackEvent):
            client_command_keyword = event.postback.data.lower()
        
        for key, command in CommandSelector.COMMAND_MAPPING.items():
            if key in client_command_keyword:
                return command(event)
            
        return MenuCommand(event)