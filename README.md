# TimeLink

TimeLine 為工作室與顧客溝通之橋樑。

顧客能透過 TimeLink LINE Bot 在 Line 群組預約工作室所提供之服務；而工作室亦能透過 TimeLink 後台管理系統，管理 Line 群組內之事務。

本系統分為兩部分:

TimeLink LINE Bot： LINE 客戶端在群組中，溝通之機器人

![TimeLink Line bot](./rm_static/demo_bot.gif)

TimeLink 後台管理系統： 工作室端用以管理 LINE 群組之後台管理系統。

<img src="https://d43czlgw2x7ve.cloudfront.net/timelink/demo_web.png" alt="TimeLink Web" width="800">

<br>

## Demo Link

### TimeLink LINE Bot

LINE 掃描 QRcode 加入 Demo 群組以使用機器人：

<img src="https://d43czlgw2x7ve.cloudfront.net/timelink/test_group_qr.JPG" alt="Group QRcode" width="200" height="200">

### TimeLink 管理系統

點此 [TimeLink 後台](https://timelink.cc) 連結

後台測試帳密：

-   username: test
-   password: test

<br>

## Technique

### Language

-   Python
    -   flask
    -   LINE Messaging API
-   HTML, CSS, JavaScript
    -   AJAX

### Backend Architecture

<img src="https://d43czlgw2x7ve.cloudfront.net/timelink/Backend_Architecture.png" alt="Backend Architecture" >

-   使用 Docker, Docker-Compose 快速部署上 AWS Ec2
-   使用 Nginx 做反向代理
-   HTTPS
-   使用 Gunicorn 作為 Flask 的 Web Server Gateway Interface
-   使用 AWS RDS 雲端 MySql 資料庫
