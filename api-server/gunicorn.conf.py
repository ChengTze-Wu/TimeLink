import os

PORT = os.environ.get("PORT", 8000)

# Description: Gunicorn configuration file
wsgi_app = "app:create_app()"
bind = f"0.0.0.0:{PORT}"
workers = 1

# Logging
accesslog = "-"
errorlog = "-"

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "info"
