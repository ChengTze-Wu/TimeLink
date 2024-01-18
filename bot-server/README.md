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
export LINE_CHANNEL_SECRET=<LINE_CHANNEL_SECRET>
export LINE_CHANNEL_ACCESS_TOKEN=<LINE_CHANNEL_ACCESS_TOKEN>
export API_SERVER_HOST=<API_SERVER_HOST>
```

### Step2. 啟動
```bash
uvicorn app.main:app
```