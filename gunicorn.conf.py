# Gunicorn configuration file for production deployment
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
enable_stdio_inheritance = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "flask_news_app"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
