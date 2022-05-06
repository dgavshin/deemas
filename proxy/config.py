import logging
import random
from os import getenv
from pathlib import Path
from re import compile
import string

# Формат флага
FLAG_FORMAT = compile(rb"([A-Z0-9]{31}=)")
FLAG_LEN = 32
# Формат флага в зашифрованном виде
ENCRYPTED_FLAG_FORMAT = compile(rb"([A-Z0-9]{31}=)")
ENCRYPTED_FLAG_LEN = 32

# Метод шифрования и его параметры
#
ENCRYPTION_MODE = {
    "name": "substitution",
    "params": {
        "skip": b"=",
        "alphabet": (string.ascii_uppercase + string.digits).encode(),
        "key": bytes(random.sample((string.ascii_uppercase + string.digits).encode(), k=FLAG_LEN))}
}

# Путь до папки с правилами
RULE_PATH = "./proxy/rules"

# Нейминг файлов с проверками:
# rule_{protocol}_{request | response}_rule_name.py
# Пример: http_decrypt_flag_count.py
RULE_NAMING = "%s_%s_%s.py"

ALLOWABLE_FLAG_COUNT = 3

# Название переменной окружения, в которой записаны правила,
# запрещенные к выполнению
# Пример: BANNED_RULES=flag_count,sql
BANNED_RULES_ENV = "BANNED_RULES"

# Название переменной окружения, в которой записано имя
# сервиса
SERVICE_NAME_ENV = "SERVICE_NAME"

MAX_LOG_BYTES = 100000

LOG_LEVEL = logging.INFO
LOG_DIR = Path("./logs")
