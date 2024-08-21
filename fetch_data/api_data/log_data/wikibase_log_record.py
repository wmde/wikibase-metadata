"""Wikibase Log Record"""

from datetime import datetime
from typing import Optional

from model.enum import WikibaseLogType, compile_log_type


class WikibaseLogRecord:
    """Wikibase Log Record"""

    id: int
    user: Optional[str]
    log_date: datetime
    log_type: WikibaseLogType

    def age(self) -> int:
        """Age in Days"""
        return (datetime.today() - self.log_date).days

    def __init__(self, record: dict):
        self.id = record["logid"]
        self.log_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        self.user = record["user"] if "user" in record else None
        self.log_type = compile_log_type(record)

    def __str__(self) -> str:
        return (
            f"WikibaseLogRecord("
            f"id={self.id}, "
            f"user={self.user}, "
            f"log_date={self.log_date}, "
            f"log_type={self.log_type})"
        )
