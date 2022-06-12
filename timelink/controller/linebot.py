import os
import model

from flask import (
    Blueprint, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, JoinEvent, MemberJoinedEvent
)

# linebot
linebot = Blueprint('linebot', __name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET_KEY'))

@linebot.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("歡迎加入我，請輸入 tl 以查看各項功能。")
    )
    
@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    line_bot_api.push_message(event.source.group_id, TextSendMessage(text=f'你好，請點選我的頭像，並加入我，\n即可開始使用TimeLink機器人!'))


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # Check if group_id in rds
    if event.message.text.lower().startswith("tl"):
        groups = model.group.get_all_groupId()["data"]
        group_ids = [group["groupId"] for group in groups]
        if event.source.group_id not in group_ids:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"此linebot尚未註冊，請至 https://timelink.cc 後台輸入：\n{event.source.group_id}\n以綁定。")
            )
        else:
            profile = line_bot_api.get_profile(event.source.user_id)
            user_name = profile.display_name
            # function
            if "服務" in event.message.text:
                groupId = model.group.get_group_id_by_groupId(event.source.group_id)
                services = model.service.get_all_by_group(groupId["data"])
                service_msg = ""
                for service in services["data"]:
                    service_msg += f"\n{service['name']} | {service['price']}元"
                
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(f"{user_name}，為您查看服務列表：{service_msg}")
                )
            elif "預約" in event.message.text:
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage("預約完成")
                )
            else:
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage("查看服務列表 請輸入：tl 服務")
                )