"""Wikibase Log Type Enum"""

import enum
import re


class WikibaseLogType(enum.Enum):
    """Wikibase Log Type"""

    ABUSE_FILTER_CREATE = 1
    COMMENTS_CREATE = 2
    COMMENTS_DELETE = 3
    CONSUMER_APPROVE = 4
    CONSUMER_PROPOSE = 5
    IMAGE_UPLOAD = 6
    IMAGE_OVERWRITE = 7
    IMPORT = 8
    INTERWIKI_CREATE = 9
    INTERWIKI_DELETE = 10
    INTERWIKI_EDIT = 11
    ITEM_CREATE = 12
    ITEM_DELETE = 13
    MOVE = 14
    PAGE_CREATE = 15
    PAGE_DELETE = 16
    PATROL = 17
    PATROL_AUTO = 18
    PROPERTY_CREATE = 19
    PROPERTY_DELETE = 20
    PROTECT = 21
    UNDO_DELETE = 22
    USER_BLOCK = 23
    USER_UNBLOCK = 24
    USER_CREATE = 25
    USER_RIGHTS = 26


def compile_log_type(record: dict) -> WikibaseLogType:
    """Compile Log Type"""

    log_type: WikibaseLogType
    match (record["type"], record["action"]):
        case ("abusefilter", "create"):
            log_type = WikibaseLogType.ABUSE_FILTER_CREATE
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
        case ("protect", "move_prot") | ("protect", "protect") | ("protect", "modify"):
            log_type = WikibaseLogType.PROTECT
        case _:
            raise NotImplementedError(record)
    return log_type
