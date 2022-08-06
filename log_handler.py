from enum import Enum, auto
import logging


class LogColor(Enum):
    BLACK = 30
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()


class LogHandler(logging.StreamHandler):
    LEVEL_COLORS = {
        logging.WARNING: LogColor.YELLOW,
        logging.ERROR: LogColor.RED,
        logging.CRITICAL: LogColor.MAGENTA,
        logging.INFO: LogColor.GREEN,
        logging.DEBUG: LogColor.BLUE,
    }

    def __init__(self) -> None:
        super().__init__()
        self.formatters = {
            lvl: logging.Formatter(
                "\033[{}m%(levelname)s\033[0m: %(message)s".format(val.value)
            )
            for lvl, val in LogHandler.LEVEL_COLORS.items()
        }
        self.formatter = self.formatters[logging.DEBUG]

    def format(self, record: logging.LogRecord) -> str:
        self.formatter = self.formatters[record.levelno]
        return self.formatter.format(record)


logger = logging.getLogger(None)
logger.addHandler(LogHandler())
logger.setLevel(logging.DEBUG)
