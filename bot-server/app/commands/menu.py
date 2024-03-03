import os
from abc import ABC, abstractmethod
from linebot.v3.webhooks import (
    GroupSource,
    UserSource
)
from linebot.v3.messaging import (
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
    URIAction,
)
from .command import Command


LIFF_URL = os.getenv("LIFF_URL")
if LIFF_URL is None:
    raise ValueError("LIFF_URL must be specified as environment variable.")


class MenuTemplate(ABC):
    @staticmethod
    @abstractmethod
    def get():
        pass


class GroupMenuTemplate(MenuTemplate):
    @staticmethod
    def get(line_group_id: str):
        return TemplateMessage(
            alt_text='TimeLink 功能表',
            template=ButtonsTemplate(
                title='TimeLink 功能表',
                text='請選擇服務項目',
                actions=[
                    PostbackAction(
                        label='熱門服務',
                        data='熱門服務'
                    ),
                    URIAction(
                        label='所有服務',
                        uri=f'{LIFF_URL}?lineGroupId={line_group_id}'
                    )
                ]
            )
        )
    

class ChatMenuTemplate(MenuTemplate):
    @staticmethod
    def get():
        return TemplateMessage(
            alt_text='TimeLink 功能表',
            template=ButtonsTemplate(
                title='TimeLink 功能表',
                text='請查看您的預約記錄',
                actions=[
                    PostbackAction(
                        label='即將到來預約',
                        data='即將到來預約'
                    ),
                ]
            )
        )


class MenuCommand(Command):
    def __init__(self, event):
        super().__init__(event)

    async def async_execute(self):
        if isinstance(self.event.source, GroupSource):
            line_group_id: str = self.event.source.group_id
            return GroupMenuTemplate.get(line_group_id)
        
        if isinstance(self.event.source, UserSource):
            return ChatMenuTemplate.get()