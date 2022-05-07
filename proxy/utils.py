import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from colorama import Fore

from config import MAX_LOG_BYTES, LOG_LEVEL


class FormatLog:

    def debug(self, message):
        self(message, Fore.GREEN, logging.DEBUG)

    def warn(self, message):
        self(message, Fore.YELLOW, logging.WARN)

    def error(self, message):
        self(message, Fore.RED, logging.ERROR)

    def info(self, message):
        self(message, Fore.GREEN, logging.INFO)

    def __call__(self, message, color, level: int = logging.INFO):
        logging.log(level, message)


def log_deemas_preview():
    logging.log(logging.INFO, ''' Mitmproxy successfully started!
        ________      _______       _______       _____ ______       ________      ________      
        |\   ___ \    |\  ___ \     |\  ___ \     |\   _ \  _   \    |\   __  \    |\   ____\     
        \ \  \_|\ \   \ \   __/|    \ \   __/|    \ \    \__\ \  \   \ \  \|\  \   \ \  \___|_    
         \ \  \  \ \   \ \  \_|/__   \ \  \_|/__   \ \   \|__| \  \   \ \   __  \   \ \_____  \   
          \ \  \_ \ \   \ \  \_|\ \   \ \  \_|\ \   \ \  \    \ \  \   \ \  \ \  \   \|____|\  \  
           \ \_______\   \ \_______\   \ \_______\   \ \__\    \ \__\   \ \__\ \__\    ____\_\  \ 
            \|_______|    \|_______|    \|_______|    \|__|     \|__|    \|__|\|__|   |\_________\\
                                                                                      \|_________|                                                               
    ''')


def configure_logging(logfile: Path):
    """
        logfile.unlink(missing_ok=True)
        logging.getLogger().setLevel(LOG_LEVEL)
        root = logging.getLogger()
        h = RotatingFileHandler(filename=logfile, mode='w', maxBytes=MAX_LOG_BYTES)
        f = logging.Formatter('%(asctime)s %(processName)-10s %(levelname)-5s --- %(message)s')
        h.setFormatter(f)
        root.addHandler(h)
        log_deemas_preview()
    """
    return


log: "FormatLog" = FormatLog()
