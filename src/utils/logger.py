import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels and entire messages."""

    LOG_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    LOG_LEVEL_ABBREVIATIONS = {
        logging.DEBUG: "DEBG",
        logging.INFO: "INFO",
        logging.WARNING: "WARN",
        logging.ERROR: "ERRO",
        logging.CRITICAL: "CRIT",
    }

    def format(self, record):
        log_color = self.LOG_COLORS.get(record.levelno, Fore.WHITE)
        level_abbr = self.LOG_LEVEL_ABBREVIATIONS.get(record.levelno, "UNKN")
        record.levelname = f"{log_color}{level_abbr}{Style.RESET_ALL}"
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"


def setup_logger(name="log", level=logging.DEBUG):

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = ColoredFormatter(
            "%(asctime)s - %(levelname)s - %(funcName)s -%(lineno)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


# Initialize the logger for the main module
log = setup_logger()
