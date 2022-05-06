import logging
from os import getenv
from pathlib import Path


class Config(object):
    TESTING = False
    LOG_LEVEL = logging.INFO
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Europe/Moscow"
    STATUS_CRON = "*/10 * * * *"
    STATUS_SCHEDULER_ENABLED = True
    ERROR_INCLUDE_MESSAGE = False
    ERROR_404_HELP = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROXY_ADDONS = {"http": Path("proxy/httpaddon.py"), "tcp": Path("proxy/tcpaddon.py")}
    LOG_DIR = Path("./logs")
    ENABLE_IPTABLES_MANAGEMENT = True
    SYSTEM_ROOT = "/"

    API_TOKEN = getenv("API_TOKEN")
    INTERFACE = getenv("INTERFACE")
    MITMDUMP_EXECUTABLE = getenv("MITMDUMP_EXECUTABLE", "./venv/bin/mitmdump")


class Windows(Config):
    SYSTEM_ROOT = "C:\Windows"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../../proxy.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENABLE_IPTABLES_MANAGEMENT = False
    LOG_LEVEL = logging.DEBUG


class Production(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///../../proxy.db"


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
    LOG_LEVEL = logging.DEBUG
