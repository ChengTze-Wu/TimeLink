from .command import Command
from linebot.v3.messaging import (
    TemplateMessage,
    ButtonsTemplate,
    URIAction,
    PostbackAction,
)

class MenuCommand(Command):
    def __init__(self, event):
        super().__init__(event)

    async def async_execute(self):
        return TemplateMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                # thumbnail_image_url='https://example.com/image.jpg',
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
                    PostbackAction(
                        label='記錄',
                        data='記錄'
                    ),
                    # URIAction(
                    #     label='URI',
                    #     uri='http://example.com/'
                    # )
                ]
            )
        )