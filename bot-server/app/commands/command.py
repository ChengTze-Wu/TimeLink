from abc import ABC, abstractmethod
from linebot.v3.webhooks import MessageEvent

class Command(ABC):
    def __init__(self, event: MessageEvent):
        self.event = event

    @abstractmethod
    async def async_execute(self):
        pass