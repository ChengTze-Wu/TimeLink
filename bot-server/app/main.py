from dotenv import load_dotenv
load_dotenv()

import os
import sys
import logging
import httpx

from fastapi import Request, FastAPI, HTTPException
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    FollowEvent,
    MessageEvent,
    JoinEvent,
    MemberJoinedEvent,
    TextMessageContent
)
from http import HTTPStatus
from .lib.webhook import AsyncWebhookHandler
from .commands.selector import CommandSelector
from .messages import ViewMessage

API_SERVER_HOST = os.getenv("API_SERVER_HOST", None)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=channel_access_token
)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
async_handler = AsyncWebhookHandler(channel_secret)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


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
        raise HTTPException(status_code=500, detail=str(e))

    return 'OK'


@async_handler.add(FollowEvent)
async def handle_member_follow(event: FollowEvent):
    try:
        reply_message = ViewMessage.WELCOME_BACK
        line_user_id: str = event.source.user_id

        async with httpx.AsyncClient() as client:
            headers = {'user-agent': 'TimeLink-Line-Bot/0.0.1'}
            user_resp = await client.get(
                f'{API_SERVER_HOST}/api/users',
                params={'line_user_id': line_user_id},
                timeout=2, 
                headers=headers
            )

        if user_resp.status_code == HTTPStatus.NOT_FOUND:
            reply_message = ViewMessage.WELCOME_NEW_USER

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@async_handler.add(JoinEvent)
async def handle_bot_join(event: JoinEvent):
    try:
        reply_message = ViewMessage.BOT_JOIN_SUCCESS
        line_group_id = event.source.group_id
        async with httpx.AsyncClient() as client:
            headers = {'user-agent': 'TimeLink-Line-Bot/0.0.1'}
            group_resp = await client.get(
                f'{API_SERVER_HOST}/api/groups', 
                params={'line_group_id': line_group_id},
                timeout=2, 
                headers=headers
            )

        if group_resp.status_code == HTTPStatus.NOT_FOUND:
            reply_message = ViewMessage.GROUP_NOT_LINKED.substitute(line_group_id=line_group_id)

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@async_handler.add(MemberJoinedEvent)
async def handle_member_join(event: MemberJoinedEvent):
    try:
        reply_message = ViewMessage.WELCOME_MEMBER_JOIN
        line_user_id = event.joined.members[0].user_id
        line_group_id = event.source.group_id

        async with httpx.AsyncClient() as client:
            headers = {'user-agent': 'TimeLink-Line-Bot/0.0.1'}
            resp = await client.post(f'{API_SERVER_HOST}/api/users/groups', 
                json={
                    'line_user_id': line_user_id,
                    'line_group_id': line_group_id
                },
                timeout=2, 
                headers=headers
            )

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@async_handler.add(MessageEvent, message=TextMessageContent)
async def handle_message(event: MessageEvent):
    try:
        command = CommandSelector().get_command(event)
        command_message = await command.async_execute()
        reply_message = command_message if command_message else event.message.text

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    except Exception as e:
        logging.error(msg=e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))