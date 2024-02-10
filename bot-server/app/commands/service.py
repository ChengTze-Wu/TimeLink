import os
from linebot.v3.messaging import (
    ImageCarouselTemplate,
    ImageCarouselColumn,
    TemplateMessage,
    URIAction,
    TextMessage,
)
from linebot.v3.webhooks import (
    GroupSource,
)
from .command import Command
from app.messages import ViewMessage
from app.utils.fetch import APIServerFetchClient


LIFF_URL = os.getenv("LIFF_URL")
if LIFF_URL is None:
    raise ValueError("LIFF_URL must be specified as environment variable.")


class ServiceCommand(Command):
    def __init__(self, event):
        super().__init__(event)
        self.fetch_client = APIServerFetchClient()

    async def async_execute(self):        
        if not isinstance(self.event.source, GroupSource):
            raise ValueError("ServiceCommand needs a GroupSource event.")

        line_group_id: str = self.event.source.group_id
        group_resp = await self.fetch_client.get(f'/api/groups/{line_group_id}/services')

        group_resp.raise_for_status()

        services: list[dict] = group_resp.json().get("services")

        if not services:
            return TextMessage(text=ViewMessage.NO_SERVICE)

        top5_services = await self.__top_by_appointment(services, top=5)

        template_message = await self.__template_message(top5_services)
        return template_message
    
    async def __top_by_appointment(self, services, top: int = 5):
        rank_services = {}
        for service in services:
            rank_services.update({
                len(service.get("appointments")): service
            })
        return [rank_services.get(key) for key in sorted(rank_services.keys(), reverse=True)][:top]

    async def __template_message(self, services: list[dict]) -> TemplateMessage:
        columns = [
            ImageCarouselColumn(
                image_url=service.get("image") or "https://via.placeholder.com/1024x1024.png?text=No+Image",
                action=URIAction(
                    label=service.get("name"),
                    uri=f"{LIFF_URL}/services/{service.get('id')}",
                )
            ) for service in services
        ]

        return TemplateMessage(
            alt_text="服務選單",
            template=ImageCarouselTemplate(columns=columns)
        )
