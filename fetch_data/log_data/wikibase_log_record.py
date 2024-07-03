"""Create Log Observation"""

from datetime import datetime


class WikibaseLogRecord:
    """Parsing Record from Tag"""

    id: int
    user: str
    log_date: datetime

    def age(self) -> int:
        """Age in Days"""
        return (datetime.now() - self.log_date).days

    def __init__(self, record: dict):
        self.id = record["logid"]

        self.log_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        self.user = record["user"]
