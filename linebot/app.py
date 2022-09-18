import os
from dotenv import load_dotenv
load_dotenv()
import model

from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    JoinEvent, MemberJoinedEvent, FollowEvent
)

timelink_bot = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET_KEY'))

@timelink_bot.route("/callback", methods=['POST'])
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


# Bot
@handler.add(FollowEvent)
def handle_follow(event):
    try:
        user_id = event.source.user_id
        
        profile = line_bot_api.get_profile(user_id)
        user_name = profile.display_name
        
        status = model.member.create(userId=user_id, name=user_name)
        
        if status == True:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"恭喜{user_name}!\n加入 TimeLink 好友！")
            )
        elif status == "Already exists":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"歡迎{user_name}!\n再次加入 TimeLink 好友！")
            )
    except Exception:
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage("伺服器錯誤，請稍候再試一次！")
        )
            
        
# Group
@handler.add(JoinEvent)
def handle_join(event):     
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("TimeLink Bot 加入成功!\n請輸入 tl 以查看各項功能。")
    )
    

# Group member
@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    try:
        userId = event.joined.members[0].user_id
        groupId = event.source.group_id
        
        status = model.manage.create(memberId=userId, groupId=groupId)

        if status == True:
            profile = line_bot_api.get_profile(userId)
            user_name = profile.display_name
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"歡迎 {user_name}\n請輸入 tl 以查看各項功能。")
            )
        elif status == "Already exists":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("歡迎再次回來！")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("請先點選 TimeLink 頭像加入好友！")
            )
    except Exception:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("伺服器錯誤，請稍候再試一次！")
        )


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.message.text.lower().startswith("tl"):
        userId=event.source.user_id
        groupId=event.source.group_id
        # Check if group_id in rds
        group_id = model.group.get_group_id_by_groupId(groupId=groupId)
        member_id = model.member.get_member_id_by_userId(userId=userId)
        if not group_id:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"此群組尚未連結 Bot，請至 https://timelink.cc 群組管理輸入 Group ID："
                                f" {groupId}")
            )
        else:
            if not member_id:
                model.manage.create(member_id=member_id, group_id=group_id)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("請先點選 TimeLink 頭像加入好友！")
                )
                return
            # ️feature
            if "服務" in event.message.text:
                # get user name
                profile = line_bot_api.get_profile(userId)
                user_name = profile.display_name
                # get group services
                services = model.service.get_all_by_group_id(group_id)
                service_msg = ""
                if services["data"]:
                    for service in services["data"]:
                        service_msg += f"\n{service['name']} | {service['price']}元"
                else:
                    service_msg = "\n此群組目前尚無服務"
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(f"{user_name}，為您查看服務列表：{service_msg}")
                )
            elif "記錄" in event.message.text:
                # get user name
                profile = line_bot_api.get_profile(userId)
                user_name = profile.display_name
                # get user reservations
                reserves = model.reserve.get_reserve_by_member_id_and_group_id(member_id=member_id, group_id=group_id)
                reserve_record = ""
                if reserves["data"]:
                    for reserve in reserves["data"]:
                        reserve_record += f"\n{reserve['serviceName']} | {reserve['bookedDateTime']}"
                else:
                    reserve_record += f"\n您尚未預約任何服務。"
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(f"{user_name}，為您查看預約記錄：{reserve_record}")
                )
            elif "預約" in event.message.text:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("https://liff.line.me/1657198810-v359xpYa")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("查看服務列表 請輸入： tl 服務\n"
                                    "預約服務 請輸入： tl 預約\n"
                                    "查詢預約記錄 請輸入： tl 記錄")
                )
                
if __name__ == "__main__":
    timelink_bot.run(port=3000, debug=True)