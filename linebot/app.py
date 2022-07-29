import os
from dotenv import load_dotenv
load_dotenv()
import model

from flask import (
    Flask, request, abort, render_template
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

# liff
@timelink_bot.route("/api/services", methods=["GET"])
def get_services():
    try:
        groupId = request.args.get("groupId")
        resp = model.service.get_all_by_groupId(groupId=groupId)
        
        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@timelink_bot.route("/api/service/<service_id>", methods=["GET"])
def get_service(service_id):
    try:
        resp = model.service.get_all_by_service_id(service_id=service_id)

        return resp
    except Exception as e:
        return {'error':str(e)}, 405
    
@timelink_bot.route("/api/available_time/<service_id>", methods=["GET"])
def get_available_time(service_id):
    try:
        resp = model.reserve.get_available_time(service_id=service_id)
        print(resp)
        return resp
    except Exception as e:
        return {'error':str(e)}, 405



@timelink_bot.route("/liff/services", methods=['GET'])
def liff_services():
    return render_template("services.html")

@timelink_bot.route("/liff/service/<service_id>", methods=['GET'])
def liff_service(service_id):
    return render_template("service.html")


# line bot
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


# Member
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    
    try:
        profile = line_bot_api.get_profile(user_id)
        user_name = profile.display_name
        
        model.member.create(userId=user_id, name=user_name)
        
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"恭喜{user_name}!\n成功啟用 TimeLink Bot。")
        )
    except Exception as e:
        if e.errno == 1062:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(f"你好{user_name}!\n你已啟用 TimeLink Bot。")
            )
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("請稍候再試一次！")
            )

@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    try:
        group_id = model.group.get_group_id_by_groupId(groupId=event.source.group_id)
        member_id = model.member.get_member_id_by_userId(userId=event.joined.members[0].user_id)
        
        resp = model.manage.create(member_id=member_id, group_id=group_id)

        line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("你已與群組 TimeLink Bot 綁定成功！")
            )
    except Exception as e:
        if e.errno == 1062:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("歡迎回來")
            )
        else:
            print(str(e))
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("請稍候再試一次！")
            )
    
# Group
@handler.add(JoinEvent)
def handle_join(event):     
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("TimeLink Bot 加入成功!\n請輸入 tl 以查看各項功能。")
    )


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.message.text.lower().startswith("tl"):
        # Check if group_id in rds
        groups = model.group.get_all_groupId()["data"]
        group_ids = [group["groupId"] for group in groups]
        
        group_id = model.group.get_group_id_by_groupId(groupId=event.source.group_id)
        member_id = model.member.get_member_id_by_userId(userId=event.source.user_id)
        
        resp = model.manage.create(member_id=member_id, group_id=group_id)
        
        if event.source.group_id not in group_ids:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"此 LineBot 尚未註冊，請至 https://timelink.cc 後台輸入："
                                f" {event.source.group_id} \n以綁定。")
            )
        else:
            # ️feature
            if "服務" in event.message.text:
                # get user name
                profile = line_bot_api.get_profile(event.source.user_id)
                user_name = profile.display_name
                # get group services
                groupId = model.group.get_group_id_by_groupId(event.source.group_id)
                
                services = model.service.get_all_by_group_id(groupId)
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
                        TextSendMessage("https://liff.line.me/1657198810-v359xpYa")
                )
            else:
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage("查看服務列表 請輸入： tl 服務\n"
                                        "預約服務 請輸入： tl 預約")
                )
                
if __name__ == "__main__":
    timelink_bot.run(port=3000, debug=True)