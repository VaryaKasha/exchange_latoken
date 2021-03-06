# -*- coding: utf-8 -*-
import os
from distutils.util import strtobool

from dotenv import load_dotenv


load_dotenv()

BOT_NAME = "exchange-latoken"

SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"
COMMANDS_MODULE = "commands"

PROXY = os.getenv("PROXY", "")
PROXY_AUTH = os.getenv("PROXY_AUTH", "")
PROXY_ENABLED = os.getenv("PROXY_ENABLED", False)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = os.getenv("CONCURRENT_REQUESTS", 16)
CONCURRENT_REQUESTS_PER_DOMAIN = os.getenv("CONCURRENT_REQUESTS_PER_DOMAIN", 8)
DOWNLOAD_DELAY = os.getenv("DOWNLOAD_DELAY", 0)
DOWNLOAD_TIMEOUT = os.getenv("DOWNLOAD_TIMEOUT", 180)

# HTTPERROR_ALLOWED_CODES = [404, 405, 407, 429, 456, 503]
HTTPERROR_ALLOW_ALL = True

# COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = False
TELNETCONSOLE_PASSWORD = "password"

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    # Upgrade-Insecure-Requests: 1
    "Cache-Control": "max-age=0",
}

# SPIDER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": None,
    "middlewares.HttpProxyMiddleware": 543,
    "middlewares.LogErrorsMiddleware": 550,
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE") if os.getenv("LOG_FILE", "") else None

# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

ITEM_PIPELINES = {
    "pipelines.ExLatPipeline": 300,
}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

MYSQL_USER = os.getenv("MYSQL_USER", "127.0.0.1")
MYSQL_PASS = os.getenv("MYSQL_PASS", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", 3306)
MYSQL_PORT = os.getenv("MYSQL_PORT", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "db_name")

PIKA_LOG_LEVEL = os.getenv("PIKA_LOG_LEVEL", "WARN")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST", "guest")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "/")

try:
    HTTPCACHE_ENABLED = strtobool(os.getenv("HTTPCACHE_ENABLED", "False"))
except ValueError:
    HTTPCACHE_ENABLED = False

HTTPCACHE_IGNORE_HTTP_CODES = list(
    map(int, (s for s in os.getenv("HTTPCACHE_IGNORE_HTTP_CODES", "").split(",") if s))
)
