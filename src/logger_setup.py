import logging
import os
import sys


USE_COLOR = (
    sys.stdout.isatty()
    and (os.environ.get("NO_COLOR", "").strip() == "")
)


class _ColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: "[36m",
        logging.WARNING: "[33m",
        logging.ERROR: "[31m",
        logging.CRITICAL: "[31;1m",
        logging.DEBUG: "[90m",
    }
    RESET = "[0m"
    DIM = "[90m"

    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%H:%M:%S")
        level = record.levelname
        message = record.getMessage()

        if USE_COLOR:
            ts = f"{self.DIM}[{timestamp}] {self.RESET}"
            level_col = self.COLORS.get(record.levelno, "")
            level_txt = f"{level_col}[{level}] {self.RESET}"
        else:
            ts = f"[{timestamp}] "
            level_txt = f"[{level}] "

        return f"{ts}{level_txt}{message}"


def get_logger(name: str):
    root = logging.getLogger()
    if (not root.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(_ColorFormatter())
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
