import logging
import os
from pathlib import Path
from logging import handlers, Logger, Formatter


data_file = Path('collectiondata', 'boardgamecollections.yml')
data_file.parent.mkdir(exist_ok=True)

log_file = Path("logs", "app.log")
log_file.parent.mkdir(exist_ok=True)

TRACE_LEVEL = logging.TRACE = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")


def monkeypatch_trace(self: logging.Logger, msg: str, *args, **kwargs) -> None:
    """Log `msg` with severity `TRACE`."""
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, msg, args, **kwargs)


Logger.trace = monkeypatch_trace

DEBUG_MODE = 'True' in os.environ.get('DEBUG_MODE')

log_level = TRACE_LEVEL if DEBUG_MODE else logging.INFO
format_string = "%(asctime)s | %(name)30s | %(levelname)8s | %(message)s"

file_handler = handlers.RotatingFileHandler(log_file, maxBytes=5242880, backupCount=5, encoding='utf8')
file_handler.setFormatter(Formatter(format_string))

root_log = logging.getLogger()
root_log.setLevel(log_level)
root_log.addHandler(file_handler)
