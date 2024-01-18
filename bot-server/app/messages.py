from string import Template

class ViewMessage:
    # static messages
    WELCOME_BACK = "歡迎回來"
    WELCOME_MEMBER_JOIN = "歡迎加入"
    BOT_JOIN_SUCCESS = "TimeLink Bot 加入成功!\n請輸入 tl 以查看各項功能。"

    # template messages
    WELCOME_NEW_USER = Template("歡迎, 您尚未加入系統, 請至 LIFF 註冊.")
    GROUP_NOT_LINKED = Template("此群組尚未連結 Bot，請至 https://timelink.cc 群組管理輸入群組 ID：$line_group_id")

