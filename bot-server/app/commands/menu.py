from abc import ABC, abstractmethod
from linebot.v3.webhooks import (
    GroupSource,
    UserSource
)
from linebot.v3.messaging import (
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
)
from .command import Command

class MenuTemplate(ABC):
    @staticmethod
    @abstractmethod
    def get():
        pass


class GroupMenuTemplate(MenuTemplate):
    @staticmethod
    def get():
        return TemplateMessage(
            alt_text='TimeLink 功能表',
            template=ButtonsTemplate(
                title='TimeLink 功能表',
                text='請選擇服務項目',
                actions=[
                    PostbackAction(
                        label='服務',
                        data='服務'
                    ),
                    PostbackAction(
                        label='預約',
                        data='預約'
                    ),
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
                text='請查看您的所有預約記錄',
                actions=[
                    PostbackAction(
                        label='預約記錄',
                        data='記錄'
                    ),
                ]
            )
        )


class MenuCommand(Command):
    def __init__(self, event):
        super().__init__(event)

    async def async_execute(self):
        if isinstance(self.event.source, GroupSource):
            return GroupMenuTemplate.get()
        
        if isinstance(self.event.source, UserSource):
            return ChatMenuTemplate.get()