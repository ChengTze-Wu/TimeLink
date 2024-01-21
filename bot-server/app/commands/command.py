from abc import ABC, abstractmethod
from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
)
from linebot.v3.messaging import (
    Message
)

class Command(ABC):
    def __init__(self, event: MessageEvent | PostbackEvent):
        self.event = event

    @abstractmethod
    async def async_execute(self) -> Message | None:
        pass