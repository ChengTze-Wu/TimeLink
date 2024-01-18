import os
import sys
import httpx

from fastapi import Request, FastAPI, HTTPException
from dotenv import load_dotenv
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
    TextMessageContent
)
from .lib.webhook import AsyncWebhookHandler
from .commands.factory import CommandFactory

load_dotenv()

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

API_SERVER_HOST = os.getenv("API_SERVER_HOST", None)

@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()

    try:
        await async_handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return 'OK'


@async_handler.add(FollowEvent)
async def handle_follow(event: FollowEvent):
    try:
        user_id = event.source.user_id
        user_profile = await line_bot_api.get_profile(user_id)
        user_name = user_profile.display_name

        print(user_id)
        print(user_profile)
        print(user_name)

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"恭喜 {user_name}!\n加入 TimeLink 好友！")]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@async_handler.add(MessageEvent, message=TextMessageContent)
async def handle_message(event: MessageEvent):
    try:
        command = CommandFactory.get_command(event.message.text)
        if command:
            command.execute()

        line_user_id: str = event.source.user_id
        async with httpx.AsyncClient() as client:
            user_resp = await client.get(f'{API_SERVER_HOST}/api/users/line/{line_user_id}')
        user_json: dict = user_resp.json()
        appointments: list = user_json.get("appointments")
        
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f'您共有 {len(appointments)} 筆預約.')]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))