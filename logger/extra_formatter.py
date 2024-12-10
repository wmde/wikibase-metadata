"""Log Format"""

import logging


DEFAULT_ARGS = {
    "name",
    "msg",
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
    "processName",
    "process",
    "wikibase",
}


class OptionalExtraFormatter(logging.Formatter):
    """Supports an optional `wikibase` extra argument"""

    def format(self, record: logging.LogRecord) -> str:
        """Format Record"""

        base_fmt = "%(asctime)s | %(levelname)s | %(message)s"
        wikibase_fmt = (
            "%(asctime)s | %(levelname)s | wikibase %(wikibase)d | %(message)s"
        )

        if "wikibase" in record.__dict__.keys():
            fmt = wikibase_fmt
        else:
            fmt = base_fmt

        for k in record.__dict__.keys():
            if k not in DEFAULT_ARGS:
                fmt += f"\n\t{k}: {record.__dict__.get(k)}"

        self._style._fmt = fmt  # pylint: disable=protected-access

        return super().format(record)
