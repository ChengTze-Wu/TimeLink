from dotenv import load_dotenv
load_dotenv()

import os
import sys
import logging
import asyncio
from contextlib import asynccontextmanager
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
from app.lib.webhook import AsyncWebhookHandler
from app.lib.fetch import APIServerFetchClient, RedisClient
from app.utils.selector import CommandSelector
from app.messages import ViewMessage

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_api_client.close()  # Close client session
    await redis_client.close()


app = FastAPI(lifespan=lifespan)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
async_handler = AsyncWebhookHandler(channel_secret)
fetch = APIServerFetchClient()
redis_client = RedisClient(ttl_seconds=60*10)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.get("/ping")
async def health_check():
    return {"status": "ok"}


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
        reply_message = ViewMessage.WELCOME_BACK
        resp = await __register_user(event.source.user_id)

        if resp and resp.status_code == HTTPStatus.CREATED:
            name = resp.json().get('name')
            reply_message = ViewMessage.WELCOME_NEW_USER.substitute(name=name)

        if reply_message:
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
        reply_message = None
        line_user_id = event.joined.members[0].user_id
        line_group_id = event.source.group_id

        resp = await fetch.post(f'/api/groups/{line_group_id}/users/{line_user_id}')

        if resp.status_code == HTTPStatus.CONFLICT:
            reply_message = ViewMessage.WELCOME_BACK

        if resp.status_code == HTTPStatus.CREATED:
            reply_message = ViewMessage.WELCOME_MEMBER_JOIN

        if reply_message:
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
        
        delete_redis_task = redis_client.delete(f'line:user:{line_user_id}:group:{line_group_id}')
        delete_api_task = fetch.delete(f'/api/groups/{line_group_id}/users/{line_user_id}')

        results = await asyncio.gather(delete_redis_task, delete_api_task)

        resp = results[1]
        resp.raise_for_status()

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
        await __register_user(event.source.user_id)
        if isinstance(event.source, GroupSource):
            if not await __check_group_linked(event):
                return
            await __connect_user_to_group(event.source.user_id, event.source.group_id)

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
        await __register_user(event.source.user_id)
        if isinstance(event.source, GroupSource):
            if not await __check_group_linked(event):
                return
            await __connect_user_to_group(event.source.user_id, event.source.group_id)

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
    line_group_id = event.source.group_id

    if await redis_client.get(f'line:group:{line_group_id}'):
        return True

    group_api_response = await fetch.get(f'/api/groups/line/{line_group_id}')

    if group_api_response.status_code == HTTPStatus.OK:
        user_command = None
        if isinstance(event, MessageEvent):
            user_command = event.message.text
        if isinstance(event, PostbackEvent):
            user_command = "/"

        is_active = group_api_response.json().get('is_active', False)
        if user_command == "/" and not is_active:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=ViewMessage.GROUP_NOT_ACTIVE)]
                )
            )
            return False

        await redis_client.set(f'line:group:{line_group_id}', 1)
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


async def __register_user(line_user_id):
    if await redis_client.get(f'line:user:{line_user_id}'):
        return

    user_profile = await line_bot_api.get_profile(line_user_id)
    user_api_response = await fetch.post('/api/users', {
        "username": line_user_id,
        "name": user_profile.display_name,
        "email": f"{line_user_id}@mail.com",
        "password": await __generate_random_password(),
        'line_user_id': line_user_id,
        'role': 'group_member'
    })

    if user_api_response.status_code in [HTTPStatus.CREATED, HTTPStatus.CONFLICT]:
        await redis_client.set(f'line:user:{line_user_id}', 1)

    return user_api_response


async def __generate_random_password(length: int = 12):
    import random
    import string
    characters = [
        random.choice(string.ascii_uppercase),  # At least one uppercase letter
        random.choice(string.ascii_lowercase),  # At least one lowercase letter
        random.choice(string.digits),  # At least one digit
        random.choice('@$!%*?&.')  # At least one special character
    ]
    characters += random.choices(string.ascii_letters + string.digits, k=length-4)
    random.shuffle(characters)
    password = ''.join(characters)
    return password


async def __connect_user_to_group(line_user_id, line_group_id):
    if await redis_client.get(f'line:user:{line_user_id}:group:{line_group_id}'):
        return True

    user_group_api_response = await fetch.post(f'/api/groups/{line_group_id}/users/{line_user_id}')
    if user_group_api_response.status_code in [HTTPStatus.CONFLICT, HTTPStatus.CREATED]:
        await redis_client.set(f'line:user:{line_user_id}:group:{line_group_id}', 1)
        return True
    return False
