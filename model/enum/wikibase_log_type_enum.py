"""Wikibase Log Type Enum"""

import enum
import re


class WikibaseLogType(enum.Enum):
    """Wikibase Log Type"""

    ABUSE_FILTER_CREATE = 1
    ABUSE_FILTER_MODIFIY = 2
    COMMENTS_CREATE = 3
    COMMENTS_DELETE = 4
    CONSUMER_APPROVE = 5
    CONSUMER_CREATE = 6
    CONSUMER_PROPOSE = 7
    CONSUMER_REJECT = 8
    CONSUMER_UPDATE = 9
    EVENT_DELETE = 10
    EXPORT_PDF = 11
    FEEDBACK_CREATE = 12
    FEEDBACK_FEATURE = 13
    FEEDBACK_FLAG = 14
    FEEDBACK_FLAG_INAPPROPRIATE = 15
    FEEDBACK_HIDE = 16
    FEEDBACK_NO_ACTION = 17
    FEEDBACK_RESOLVE = 18
    IMPORT = 19
    INTERWIKI_CREATE = 20
    INTERWIKI_DELETE = 21
    INTERWIKI_EDIT = 22
    ITEM_CREATE = 23
    ITEM_DELETE = 24
    MEDIA_OVERWRITE = 25
    MEDIA_REVERT = 26
    MEDIA_UPLOAD = 27
    MOVE = 28
    PAGE_CREATE = 29
    PAGE_DELETE = 30
    PATROL = 31
    PATROL_AUTO = 32
    PROFILE = 33
    PROPERTY_CREATE = 34
    PROPERTY_DELETE = 35
    PROTECT = 36
    REVISION_DELETE = 37
    TAG_CREATE = 38
    UNDO_DELETE = 39
    UNPROTECT = 40
    USER_BLOCK = 41
    USER_UNBLOCK = 42
    USER_CREATE = 43
    USER_DELETE = 44
    USER_MERGE = 45
    USER_RENAME = 46
    USER_RIGHTS = 47
    WIKI_FARM = 48
    WIKI_NAMESPACES = 49
    WIKI_RIGHTS = 50
    WIKI_SETTINGS = 51


MEDIA_REGEX = re.compile(r".*\.(flv|jpg|png)", re.IGNORECASE)
ITEM_REGEX = re.compile(r"Item:Q\d+")
PROPERTY_REGEX = re.compile(r"(Property|WikibaseProperty):P\d+")


# pylint: disable=too-many-statements
def compile_log_type(record: dict) -> WikibaseLogType:
    """Compile Log Type"""

    log_type: WikibaseLogType
    match (record["type"], record["action"]):
        case ("create", "create"):
            if ITEM_REGEX.match(record["title"]) is not None:
                log_type = WikibaseLogType.ITEM_CREATE
            elif PROPERTY_REGEX.match(record["title"]) is not None:
                log_type = WikibaseLogType.PROPERTY_CREATE
            else:
                log_type = WikibaseLogType.PAGE_CREATE
        case ("delete", "delete"):
            if ITEM_REGEX.match(record["title"]):
                log_type = WikibaseLogType.ITEM_DELETE
            elif PROPERTY_REGEX.match(record["title"]) is not None:
                log_type = WikibaseLogType.PROPERTY_DELETE
            else:
                log_type = WikibaseLogType.PAGE_DELETE
        case ("abusefilter", "create"):
            log_type = WikibaseLogType.ABUSE_FILTER_CREATE
        case ("abusefilter", "modify"):
            log_type = WikibaseLogType.ABUSE_FILTER_MODIFIY
        case ("comments", "add"):
            log_type = WikibaseLogType.COMMENTS_CREATE
        case ("comments", "delete"):
            log_type = WikibaseLogType.COMMENTS_DELETE
        case ("mwoauthconsumer", "approve"):
            log_type = WikibaseLogType.CONSUMER_APPROVE
        case ("mwoauthconsumer", "create-owner-only"):
            log_type = WikibaseLogType.CONSUMER_CREATE
        case ("mwoauthconsumer", "propose"):
            log_type = WikibaseLogType.CONSUMER_PROPOSE
        case ("mwoauthconsumer", "reject"):
            log_type = WikibaseLogType.CONSUMER_REJECT
        case ("mwoauthconsumer", "update"):
            log_type = WikibaseLogType.CONSUMER_UPDATE
        case ("delete", "event"):
            log_type = WikibaseLogType.EVENT_DELETE
        case ("pdf", "book"):
            log_type = WikibaseLogType.EXPORT_PDF
        case ("articlefeedbackv5", "create"):
            log_type = WikibaseLogType.FEEDBACK_CREATE
        case ("articlefeedbackv5", "feature"):
            log_type = WikibaseLogType.FEEDBACK_FEATURE
        case ("articlefeedbackv5", "flag"):
            log_type = WikibaseLogType.FEEDBACK_FLAG
        case ("articlefeedbackv5", "inappropriate"):
            log_type = WikibaseLogType.FEEDBACK_FLAG_INAPPROPRIATE
        case ("articlefeedbackv5", "hide"):
            log_type = WikibaseLogType.FEEDBACK_HIDE
        case ("articlefeedbackv5", "noaction"):
            log_type = WikibaseLogType.FEEDBACK_NO_ACTION
        case ("articlefeedbackv5", "resolve"):
            log_type = WikibaseLogType.FEEDBACK_RESOLVE
        case ("import", "upload"):
            log_type = WikibaseLogType.IMPORT
        case ("interwiki", "iw_add"):
            log_type = WikibaseLogType.INTERWIKI_CREATE
        case ("interwiki", "iw_delete"):
            log_type = WikibaseLogType.INTERWIKI_DELETE
        case ("interwiki", "iw_edit"):
            log_type = WikibaseLogType.INTERWIKI_EDIT
        case ("upload", "overwrite"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_OVERWRITE
            else:
                raise NotImplementedError(record)
        case ("upload", "revert"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_REVERT
            else:
                raise NotImplementedError(record)
        case ("upload", "upload"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_UPLOAD
            else:
                raise NotImplementedError(record)
        case ("move", "move"):
            log_type = WikibaseLogType.MOVE
        case ("patrol", "autopatrol"):
            log_type = WikibaseLogType.PATROL_AUTO
        case ("patrol", "patrol"):
            log_type = WikibaseLogType.PATROL
        case ("profile", "profile"):
            log_type = WikibaseLogType.PROFILE
        case ("protect", "move_prot") | ("protect", "protect") | ("protect", "modify"):
            log_type = WikibaseLogType.PROTECT
        case ("delete", "revision"):
            log_type = WikibaseLogType.REVISION_DELETE
        case ("managetags", "create"):
            log_type = WikibaseLogType.TAG_CREATE
        case ("delete", "restore"):
            log_type = WikibaseLogType.UNDO_DELETE
        case ("protect", "unprotect"):
            log_type = WikibaseLogType.UNPROTECT
        case ("block", "block") | ("block", "reblock"):
            log_type = WikibaseLogType.USER_BLOCK
        case ("block", "unblock"):
            log_type = WikibaseLogType.USER_UNBLOCK
        case (
            ("newusers", "autocreate")
            | ("newusers", "byemail")
            | ("newusers", "create")
            | ("newusers", "create2")
        ):
            log_type = WikibaseLogType.USER_CREATE
        case ("usermerge", "deleteuser"):
            log_type = WikibaseLogType.USER_DELETE
        case ("usermerge", "mergeuser"):
            log_type = WikibaseLogType.USER_MERGE
        case ("rights", "rights") | ("rights", "blockautopromote"):
            log_type = WikibaseLogType.USER_RIGHTS
        case ("renameuser", "renameuser"):
            log_type = WikibaseLogType.USER_RENAME
        case ("farmer", "managewiki"):
            log_type = WikibaseLogType.WIKI_FARM
        case ("managewiki", "namespaces"):
            log_type = WikibaseLogType.WIKI_NAMESPACES
        case ("managewiki", "rights"):
            log_type = WikibaseLogType.WIKI_RIGHTS
        case ("managewiki", "settings"):
            log_type = WikibaseLogType.WIKI_SETTINGS
        case _:
            raise NotImplementedError(record)
    return log_type
