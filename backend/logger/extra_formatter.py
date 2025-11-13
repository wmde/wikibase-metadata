"""Log Format"""

import logging


DEFAULT_ARGS = {
    "name",
    "msg",
    "message",
    "asctime",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "taskName",
    "processName",
    "process",
    "wikibase",
}


class OptionalExtraFormatter(logging.Formatter):
    """Supports an optional `wikibase` extra argument"""

    def format(self, record: logging.LogRecord) -> str:
        """Format Record"""

        fmt = "%(asctime)s | "

        if record.levelno == logging.ERROR:
            fmt += "ERR  | "
        elif record.levelno == logging.WARNING:
            fmt += "WARN | "
        elif record.levelno == logging.INFO:
            fmt += "INFO | "
        elif record.levelno == logging.DEBUG:
            fmt += "DBG  | "
        elif record.levelno == logging.CRITICAL:
            fmt += "CRIT | "

        if "taskName" in record.__dict__.keys():
            fmt += "%(taskName)s | "

        if "wikibase" in record.__dict__.keys():
            fmt += "wikibase:%(wikibase)d | "

        fmt += "%(message)s"

        for k in record.__dict__.keys():
            if k not in DEFAULT_ARGS:
                fmt += f" | {k}:{record.__dict__.get(k)}"

        self._style._fmt = fmt  # pylint: disable=protected-access

        return super().format(record)
