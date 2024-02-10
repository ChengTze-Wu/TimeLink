from dotenv import load_dotenv
load_dotenv()

import os
import sys
import logging
import httpx
import requests

from fastapi import Request, FastAPI, HTTPException
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    JoinEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
    PostbackEvent,
    TextMessageContent,
    Event,
    GroupSource,
)
from http import HTTPStatus
from .lib.webhook import AsyncWebhookHandler
from .utils.fetch import APIServerFetchClient
from .selector import CommandSelector
from .messages import ViewMessage

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=channel_access_token,
)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
async_handler = AsyncWebhookHandler(channel_secret)
fetch = APIServerFetchClient()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.get("/ping-line-api")
async def ping_line_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.line.me/v2/bot/message/ping', headers={
                'Authorization': f'Bearer {channel_access_token}'
            })
        return {"status": "OK"}
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/ping-bun")
async def ping_line_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://bun-demo.chengtze.cc/')
        return {"status": "OK", "response": response.text}
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/sync-ping-bun")
def sync_ping_line_api():
    try:
        response =  requests.get('https://bun-demo.chengtze.cc/')
        return {"status": "OK", "response": response.text}
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()

    try:
        await async_handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return 'OK'


@async_handler.add(FollowEvent)
async def handle_member_follow(event: FollowEvent):
    try:
        line_user_id: str = event.source.user_id

        user_resp = await fetch.get(f'/api/users/{line_user_id}')

        reply_message = ViewMessage.WELCOME_BACK

        if user_resp.status_code == HTTPStatus.NOT_FOUND:
            reply_message = ViewMessage.WELCOME_NEW_USER

        if user_resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            return

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@async_handler.add(MemberJoinedEvent)
async def handle_member_join(event: MemberJoinedEvent):
    try:
        reply_message = ViewMessage.WELCOME_MEMBER_JOIN
        line_user_id = event.joined.members[0].user_id
        line_group_id = event.source.group_id

        resp = await fetch.post('/api/groups/users', {
            'line_user_id': line_user_id,
            'line_group_id': line_group_id
        })

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@async_handler.add(MemberLeftEvent)
async def handle_member_left(event: MemberLeftEvent):
    try:
        line_user_id = event.left.members[0].user_id
        line_group_id = event.source.group_id

        resp = await fetch.delete('/api/groups/users', {
            'line_user_id': line_user_id,
            'line_group_id': line_group_id
        })

    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@async_handler.add(JoinEvent)
async def handle_bot_join(event: JoinEvent):
    try:
        if not await __check_group_linked(event):
            return

        reply_message = ViewMessage.BOT_JOIN_SUCCESS
        
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@async_handler.add(MessageEvent, message=TextMessageContent)
async def handle_message(event: MessageEvent):
    try:
        if not await __check_group_linked(event):
            return

        command = CommandSelector.get_command(event)
        reply_message = await command.async_execute()

        if reply_message:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[reply_message]
                )
            )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@async_handler.add(PostbackEvent)
async def handle_postback(event: PostbackEvent):
    try:
        if not await __check_group_linked(event):
            return

        command = CommandSelector.get_command(event)
        reply_message = await command.async_execute()
        
        if reply_message:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[reply_message]
                )
            )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def __check_group_linked(event: Event):
    '''Check if the group is linked to the TimeLink System.
    If not, notify the message to line.
    '''
    if not isinstance(event.source, GroupSource):
        return True

    line_group_id = event.source.group_id
    group_api_response = await fetch.get(f'/api/groups/{line_group_id}')

    if group_api_response.status_code == HTTPStatus.OK:
        return True

    if group_api_response.status_code == HTTPStatus.NOT_FOUND:
        unbound_group_message = ViewMessage.GROUP_NOT_LINKED.substitute(line_group_id=line_group_id)
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=unbound_group_message)]
            )
        )
        return False

    return False
