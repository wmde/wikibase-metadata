"""Create Log Observation"""

from datetime import datetime
import re
from typing import Optional

from model.enum import WikibaseLogType


class WikibaseLogRecord:
    """Parsing Record from Tag"""

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


def compile_log_type(record: dict) -> WikibaseLogType:
    """Compile Log Type"""

    log_type: WikibaseLogType
    match (record["type"], record["action"]):
        case ("comments", "add"):
            log_type = WikibaseLogType.COMMENTS_CREATE
        case ("comments", "delete"):
            log_type = WikibaseLogType.COMMENTS_DELETE
        case ("interwiki", "iw_add"):
            log_type = WikibaseLogType.INTERWIKI_CREATE
        case ("interwiki", "iw_delete"):
            log_type = WikibaseLogType.INTERWIKI_DELETE
        case ("interwiki", "iw_edit"):
            log_type = WikibaseLogType.INTERWIKI_EDIT
        case ("create", "create"):
            if re.match(r"Item:Q\d+", record["title"]) is not None:
                log_type = WikibaseLogType.ITEM_CREATE
            elif re.match(r"WikibaseProperty:P\d+", record["title"]) is not None:
                log_type = WikibaseLogType.PROPERTY_CREATE
            else:
                log_type = WikibaseLogType.PAGE_CREATE
        case ("newusers", "byemail") | ("newusers", "create") | ("newusers", "create2"):
            log_type = WikibaseLogType.USER_CREATE
        case ("delete", "delete"):
            if re.match(r"Item:Q\d+", record["title"]):
                log_type = WikibaseLogType.ITEM_DELETE
            elif (
                re.match(r"WikibaseProperty:P\d+", record["title"]) is not None
                or re.match(r"Property:P\d+", record["title"]) is not None
            ):
                log_type = WikibaseLogType.PROPERTY_DELETE
            else:
                log_type = WikibaseLogType.PAGE_DELETE
        case ("delete", "restore"):
            log_type = WikibaseLogType.UNDO_DELETE
        case ("move", "move"):
            log_type = WikibaseLogType.MOVE
        case ("import", "upload"):
            log_type = WikibaseLogType.IMPORT
        case ("upload", "upload"):
            if "img_sha1" in record["params"]:
                log_type = WikibaseLogType.IMAGE_UPLOAD
            else:
                raise NotImplementedError(record)
        case ("upload", "overwrite"):
            if "img_sha1" in record["params"]:
                log_type = WikibaseLogType.IMAGE_OVERWRITE
            else:
                raise NotImplementedError(record)
        case ("patrol", "autopatrol"):
            log_type = WikibaseLogType.PATROL_AUTO
        case ("patrol", "patrol"):
            log_type = WikibaseLogType.PATROL
        case ("block", "block"):
            log_type = WikibaseLogType.USER_BLOCK
        case ("block", "unblock"):
            log_type = WikibaseLogType.USER_UNBLOCK
        case ("rights", "rights"):
            log_type = WikibaseLogType.USER_RIGHTS
        case ("mwoauthconsumer", "approve"):
            log_type = WikibaseLogType.CONSUMER_APPROVE
        case ("mwoauthconsumer", "propose"):
            log_type = WikibaseLogType.CONSUMER_PROPOSE
        case ("protect", "move_prot"):
            log_type = WikibaseLogType.PROTECT
        case _:
            raise NotImplementedError(record)
    return log_type
