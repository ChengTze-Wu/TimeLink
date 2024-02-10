# Description: Gunicorn configuration file
wsgi_app = "app:create_app()"
bind = "0.0.0.0:8000"
workers = 1

# Logging
accesslog = "app/logs/access.log"
errorlog = "app/logs/error.log"

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "info"
