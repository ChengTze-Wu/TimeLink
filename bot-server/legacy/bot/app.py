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
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    JoinEvent, MemberJoinedEvent, FollowEvent,
    ButtonsTemplate, TemplateSendMessage,
    MessageAction, URIAction, CarouselColumn,
    CarouselTemplate
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
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("請先點選 TimeLink 頭像加入好友！")
                )
                return
            model.manage.create(member_id=member_id, group_id=group_id)
            # ️feature
            if "服務" in event.message.text:
                # get group services
                services = model.service.get_all_by_group_id(group_id)
                if services["data"]:
                    carousel_columns = []
                    for service in services["data"]:
                        carousel_columns.append(
                            CarouselColumn(text=f'${service["price"]}',title=service["name"], thumbnail_image_url=service["image"], actions=[
                                URIAction(label='點此預約', uri=f'https://liff.line.me/1657198810-v359xpYa/{service["id"]}')
                            ], image_size="contain"),
                        )
                    carousel_template = CarouselTemplate(columns=carousel_columns)
                    template_message = TemplateSendMessage(
                        alt_text='查看現有服務', template=carousel_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage("此群組目前尚無服務。"))
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
                buttons_template = ButtonsTemplate(
                    text='TimeLink 預約系統', actions=[
                        URIAction(label='點此進入', uri='https://liff.line.me/1657198810-v359xpYa'),
                    ])
                template_message = TemplateSendMessage(
                    alt_text='TimeLink 預約系統', template=buttons_template)
                line_bot_api.reply_message(event.reply_token, template_message)
            else:
                buttons_template = ButtonsTemplate(
                    text='TimeLink 功能表', actions=[
                        MessageAction(label='查看現有服務', text='tl服務'),
                        MessageAction(label='查看預約記錄', text='tl記錄'),
                        MessageAction(label='預約服務', text='tl預約'),
                    ])
                template_message = TemplateSendMessage(
                    alt_text='TimeLink 功能表', template=buttons_template)
                line_bot_api.reply_message(event.reply_token, template_message)
                
if __name__ == "__main__":
    timelink_bot.run(port=3000, debug=True)