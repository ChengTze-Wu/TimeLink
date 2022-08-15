# TimeLink

TimeLine is the bridge between studios and customers.

Customers can view the services provided by the studio in the Line group through the TimeLink LINE Bot, and the studio can also manage the affairs in the Line group through the TimeLink management system.

The system can manage robots in multiple groups, and each robot can have different service information. The system is divided into two parts:

-   <h3>TimeLink LINE Bot</h3>

    <img style="margin: 16px" src="./rm_static/demo_bot.gif" alt="TimeLink Web" width="300">
    <img style="margin: 16px" src="./rm_static/booking.gif" alt="TimeLink Web" width="300">

-   <h3>TimeLink Management System</h3>

      <img src="https://d43czlgw2x7ve.cloudfront.net/timelink/demo_web.png" alt="TimeLink Web" width="800">

<br>

## Management System Link

[TimeLink](https://timelink.cc)

-   Test User for Login：
    -   Username: test
    -   Password: test

<br>

## Technique

### Backend Architecture Diagram

<img src="https://d43czlgw2x7ve.cloudfront.net/timelink/Backend_Architecture.png" alt="Backend Architecture" >

-   Powered by <b>Flask</b>
-   Following <b>Factory pattern</b> for using different configuration for different web app environments.
-   Following the <b>MVC pattern</b>, the website is divided into three parts:
    -   Model: the data layer, containing the database connection and operations.
    -   View: the presentation layer, containing the HTML templates and static files.
    -   Controller: the business logic layer, containing the api calls and the business logic.
-   Using <b>Docker</b> for containerization, <b>Docker Compose</b> for deployment.
-   Using <b>Gunicorn</b> for Web Server Gateway Interface, <b>Nginx</b> for reverse proxy and SSL certificate.
-   Using <b>AWS RDS</b> (MySQL) for database, EC2 for server.
-   Support <b>SSL</b> for HTTPS,
-   Using <b>Line Messaging API</b> on LINE Bot Server.
