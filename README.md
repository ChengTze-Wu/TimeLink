<p align="center">
  <img src="https://storage.googleapis.com/timelink-assets/TimeLink-Logo.png" alt="TimeLink" style="width: 120px;">
</p>
<p align="center">
    <em>連接消費者與商家之間的橋樑。以 Line 群組機器人簡便預約。平台即可管理服務。</em>
</p>

# TimeLink 2.0
TimeLink 是一個連接消費者與商家之間的橋樑。消費者可以透過 Line 群組機器人簡便預約服務，商家可以透過平台管理服務。TimeLink 2.0 版本是 TimeLink 1.0 版本的重構版本，將應用拆分模組，提高程式的可讀性、可維護性、可擴展性，並且使用更多的雲端服務，以提高系統的效能與安全性。

- 各模組:
  - [API Server](api-server) : 作為整個系統的核心，處理商業邏輯，並與資料庫溝通。
  - [Web Frontend](web_app) : 提供商家管理服務的介面。
  - [LIFF Frontend](liff-server) : 提供消費者預約服務的介面。
  - [Line Bot](bot-server) : 提供消費者在 Line 群組中的機器人介面。

## 改動
相較於 2022 年 [TimeLink 1.0](https://github.com/ChengTze-Wu/TimeLink/tree/v1.0.0) 版本，TimeLink 2.0 版本有以下改動：

### 程式架構
- 將原本單一的應用伺服器拆分為 API Server、Web 前端、LIFF 前端、Line Bot 等模組，使得各個模組可以獨立部署。
- API Server 相較於先前做了分層，以提高程式的可讀性與可維護性。增加使用 sqlalchemy 作為 ORM，alembic 作為資料庫版控工具。
- Web 和 LIFF 前端選用 React Next.js 框架，以更模組化的方式撰寫前端程式。
- Line Bot 改以非同步方式撰寫，以處理更多的使用者同時操作。


### 雲伺服器架構
<img src="https://storage.googleapis.com/timelink-assets/TimeLink-Architecture.png" alt="TimeLink 2.0 Server Architecture" style="width: 100%;">
- 將原本使用 EC2 VM 作為伺服器，改使用 GCP Cloud Run 作為伺服器，它可以自動擴展 instance，再不需要時自動縮減 instance，以節省成本。
- 使用 GCP Cloud Build 作為 CD 工具，監控此 Repository 的更動，並自動部署到 GCP Cloud Run。
- API Server 只開放從 VPC 流入流量，以提高伺服器的安全性。
- 使用 GCP Cloud SQL 作為資料庫，設在 VPC，且只讓 API Server 可以存取，以提高資料庫的安全性。
- 使用 GCP Cloud Storage 作為靜態檔案存放，以提高伺服器的效能。
