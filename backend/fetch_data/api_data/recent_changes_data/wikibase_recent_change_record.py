"""Wikibase Recent Change Record"""

from datetime import datetime

from logger import logger


class WikibaseRecentChangeRecord:
    """Wikibase Recent Change Record"""

    type: str
    timestamp: datetime
    user: str  # username, IP, or __generated_user_string__user:<USERID>

    def __init__(self, record: dict):
        self.type = record["type"]
        self.timestamp = datetime.fromisoformat(record["timestamp"])

        # The user field can be missing, we derive it from the userid then. More info:
        # - https://www.mediawiki.org/wiki/API:RecentChanges
        # - https://doc.wikimedia.org/mediawiki-core/1.43.1/php/classRevisionDeleteUser.html#details
        if "user" in record:
            self.user = record["user"]
        elif "userid" in record:
            self.user = f"__generated_user_string__user:{record['userid']}"
        else:
            logger.warning(
                f"No user or userid found in record: {record}, setting to __unknown_user__"
            )
            self.user = "__unknown_user__"

    def __str__(self) -> str:
        return (
            f"WikibaseRecentChangeRecord("
            f"type={self.type}, "
            f"user={self.user}, "
            f"timestamp={self.timestamp})"
        )
