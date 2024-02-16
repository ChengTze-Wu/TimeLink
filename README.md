# TimeLink 2.0
TimeLink 是一個提供消費者與商家之間的預約服務系統。消費者可以透過 Line 群組中的機器人做服務預約，而商家可以透過平台管理服務。

相較於 2022 年 [TimeLink 1.0](https://github.com/ChengTze-Wu/TimeLink/tree/v1.0.0) 版本，TimeLink 2.0 版本有以下改動：

### 程式架構改動
1. 原本 TimeLink 為單一的應用伺服器，整合了 API, Web 前端, LIFF 前端, 現將其拆分開來，使得各個模組可以獨立部署。
    - 各模組 README:
        - [API Server](api-server/README.md) : 作為整個系統的核心，處理商業邏輯，並與資料庫溝通。
        - [Web Frontend](web_app/README.md) : 提供商家管理服務的介面。
        - [LIFF Frontend](liff-server/README.md) : 提供消費者預約服務的介面。
        - [Line Bot](bot-server/README.md) : 提供消費者在 Line 群組中的機器人介面。
2. API Server 相較於先前做了分層，以提高程式的可讀性與可維護性。增加使用 sqlalchemy 作為 ORM，alembic 作為資料庫版控工具。
3. Web 和 LIFF 前端選用 React Next.js 框架，以更模組化的方式撰寫前端程式。
4. Line Bot 改以非同步方式撰寫，以處理更多的使用者同時操作。
5. 更妥善處理 Error 及 Log。

### 伺服器架構改動
1. 原本使用 EC2 VM 作為伺服器，現改使用 GCP Cloud Run 作為伺服器，它可以自動擴展 instance，再不需要時自動縮減 instance，以節省成本。
2. 使用 GCP Cloud Build 作為 CI/CD 工具，監控此 Repository 的更動，並自動部署到 GCP Cloud Run。
3. API Server 只開放從 VPC 流入流量，以提高伺服器的安全性。
4. 使用 GCP Cloud SQL 作為資料庫，設在 VPC，且只讓 API Server 可以存取，以提高資料庫的安全性。
5. 使用 GCP Cloud Storage 作為靜態檔案存放，以提高伺服器的效能。

### Local Dev 啟用方式
#### 環境變數設定
TBD.

#### Docker Compose 啟用
```bash
docker-compose up -d
```