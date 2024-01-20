# TimeLink BOT Server

TimeLink BOT Server 是 TimeLink 預約系統的 Line 機器人，用來引入 Line 群組中，協助群組成員預約服務。

## 安裝方式
### Step1. 使用 [git](https://git-scm.com/) 下載專案
```bash
git clone 
```

### Step2. 安裝相依套件
您可以使用 [pip](https://pip.pypa.io/en/stable/) 或者是 [poetry]() 套件管理工具.

#### pip 安裝
```bash
pip install -r requirements.txt
```

#### poetry 安裝
```bash
poetry install
```

## 啟用方式
### Step1. 環境變數
共需要 LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, API_SERVER_HOST
```bash
export BOT_VERSION=<BOT_VERSION>
export LINE_CHANNEL_SECRET=<LINE_CHANNEL_SECRET>
export LINE_CHANNEL_ACCESS_TOKEN=<LINE_CHANNEL_ACCESS_TOKEN>
export API_SERVER_HOST=<API_SERVER_HOST>
```

### Step2. 啟動
```bash
uvicorn app.main:app
```

## 自製套件
因目前 Line 官方尚未有非同步版本的 `WebhookHandler`, 所以就繼承它來覆寫小修改一下, 以配合非同步 handle function 使用, 為 `AsyncWebhookHandler` 放在 `/app/lib/webhook.py` 中. 歡迎參考取用.

### 使用範例
```python
async_handler = AsyncWebhookHandler(channel_secret)

@async_handler.add(MessageEvent, message=TextMessageContent)
async def handle_message(event: MessageEvent):
    pass

@async_handler.add(FollowEvent)
async def handle_follow(event: FollowEvent):
    pass
```