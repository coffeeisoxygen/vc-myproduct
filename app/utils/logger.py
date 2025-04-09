import atexit
import logging
import os
import sys
from logging.handlers import QueueHandler, QueueListener, TimedRotatingFileHandler
from queue import Queue

from colorama import Fore, Style
from colorama import init as colorama_init
from dotenv import load_dotenv

# === INIT ===
colorama_init(autoreset=True)
load_dotenv()

# === CONFIG ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


# === WARNA CONSOLE ===
def colorize(level, message):
    color_map = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }
    return f"{color_map.get(level, '')}{message}{Style.RESET_ALL}"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        original = super().format(record)
        return colorize(record.levelname, original)


# === FORMATTER ===
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATEFMT)
color_formatter = ColorFormatter(FORMAT, DATEFMT)

# === FILE HANDLER ===
# Tambahkan ekstensi .log pada file utama
log_file = os.path.join(LOG_DIR, "app.log")
file_handler = TimedRotatingFileHandler(
    filename=log_file,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
    utc=False,
)
file_handler.suffix = "-%Y%m%d"  # Rotasi akan menghasilkan app.log-20250409
file_handler.setFormatter(formatter)
file_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# === CONSOLE HANDLER ===
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(color_formatter)
console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# === QUEUE HANDLER ===
log_queue = Queue()
queue_handler = QueueHandler(log_queue)
listener = QueueListener(
    log_queue, file_handler, console_handler, respect_handler_level=True
)
listener.start()

# Register listener.stop() to be called when Python exits
atexit.register(listener.stop)


# === FUNGSI LOGGER ===
def get_logger(name="otomax-addon") -> logging.Logger:
    logger = logging.getLogger(name)

    if not getattr(logger, "_custom_configured", False):
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        logger.addHandler(queue_handler)  # Cukup gunakan queue_handler saja
        logger.propagate = False  # cegah tabrakan ke root logger (FastAPI dsb)
        setattr(logger, "_custom_configured", True)  # penanda udah di-setup

    return logger
