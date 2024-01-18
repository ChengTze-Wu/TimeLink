from .record import RecordCommand
from .reserve import ReserveCommand
from .service import ServiceCommand

class CommandFactory:
    @staticmethod
    def get_command(message_text):
        if message_text.lower().startswith("tl"):
            if "服務" in message_text:
                return ServiceCommand()
            elif "記錄" in message_text:
                return RecordCommand()
            elif "預約" in message_text:
                return ReserveCommand()
            else:
                return None