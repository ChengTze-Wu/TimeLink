from string import Template

class ViewMessage:
    # static messages
    WELCOME_BACK = "歡迎回來"
    WELCOME_MEMBER_JOIN = "歡迎加入"
    BOT_JOIN_SUCCESS = "TimeLink Bot 加入成功!\n請輸入 tl 以查看各項功能。"
    USER_NOT_LINKED = "請點選 TimeLink 頭像加入好友！並完成註冊。"
    NO_RECORD = "你尚未有預約"
    NO_COMING_RECORD = "你尚未有即將到來的預約"
    NO_SERVICE = "本群組尚未有服務"
    
    # template messages
    WELCOME_NEW_USER = Template("歡迎, 您尚未加入系統, 請至 LIFF 註冊.")
    GROUP_NOT_LINKED = Template("此群組尚未連結 Bot，請至 https://timelink.chengtze.cc 群組管理輸入群組 ID：$line_group_id")
    RECORD = Template("你共有 $count 筆預約\n$appointments")
    MOST_COMING_RECORD = Template("您的即將到來預約是：\n$service_name 將於 $reserved_at 開始, 服務費用為 $price 元")