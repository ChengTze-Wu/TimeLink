bind = "0.0.0.0:8000"
workers = 2

# log
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "./logs/access.log"
errorlog = "./logs/error.log"