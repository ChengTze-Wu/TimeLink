bind = "127.0.0.1:8000"
workers = 2

# log
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "./access.log"
errorlog = "./error.log"