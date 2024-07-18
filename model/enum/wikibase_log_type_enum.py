"""Wikibase Log Type Enum"""

import enum
import re
from typing import Optional


class WikibaseLogType(enum.Enum):
    """Wikibase Log Type"""

    ABUSE_FILTER_CREATE = 1
    ABUSE_FILTER_MODIFIY = 2
    APPROVE = 3
    COMMENTS_CREATE = 4
    COMMENTS_DELETE = 5
    CONSUMER_APPROVE = 6
    CONSUMER_CREATE = 7
    CONSUMER_DISABLE = 8
    CONSUMER_PROPOSE = 9
    CONSUMER_REJECT = 10
    CONSUMER_UPDATE = 11
    CONTENT_MODEL_CREATE = 12
    CONTENT_MODEL_CHANGE = 13
    DATADUMP_DELETE = 14
    DATADUMP_GENERATE = 15
    EVENT_DELETE = 16
    EXPORT_PDF = 17
    FEEDBACK_CREATE = 18
    FEEDBACK_FEATURE = 19
    FEEDBACK_FLAG = 20
    FEEDBACK_FLAG_INAPPROPRIATE = 21
    FEEDBACK_HIDE = 22
    FEEDBACK_NO_ACTION = 23
    FEEDBACK_RESOLVE = 24
    IMPORT = 25
    IMPORT_HTML = 26
    INTERWIKI_CREATE = 27
    INTERWIKI_DELETE = 28
    INTERWIKI_EDIT = 29
    ITEM_CREATE = 30
    ITEM_DELETE = 31
    MEDIA_APPROVE = 32
    MEDIA_OVERWRITE = 33
    MEDIA_REVERT = 34
    MEDIA_UPLOAD = 35
    MOVE = 36
    PAGE_CREATE = 37
    PAGE_DELETE = 38
    PAGE_TRANSLATE = 39
    PAGE_TRANSLATE_DELETE_FOK = 40
    PAGE_TRANSLATE_DELETE_LOK = 41
    PAGE_TRANSLATE_MARK = 42
    PAGE_TRANSLATE_UNMARK = 43
    PAGE_UPDATE_LANGUAGE = 44
    PATROL = 45
    PATROL_AUTO = 46
    PROFILE = 47
    PROPERTY_CREATE = 48
    PROPERTY_DELETE = 49
    PROTECT = 50
    REDIRECT_DELETE = 51
    REDIRECT_MOVE = 52
    REVISION_DELETE = 53
    TABLE_CREATE = 54
    TABLE_DELETE = 55
    TAG_CREATE = 56
    THANK = 57
    UNAPPROVE = 58
    UNDO_DELETE = 59
    UNPROTECT = 60
    USER_BLOCK = 61
    USER_UNBLOCK = 62
    USER_CREATE = 63
    USER_DELETE = 64
    USER_MERGE = 65
    USER_RENAME = 66
    USER_RIGHTS = 67
    WIKI_FARM = 68
    WIKI_GROUP_DELETE = 69
    WIKI_NAMESPACES = 70
    WIKI_RIGHTS = 71
    WIKI_SETTINGS = 72


MEDIA_REGEX = re.compile(r".*\.(flv|gif|jpg|pdf|png|svg)", re.IGNORECASE)
ITEM_REGEX = re.compile(r"Item:Q\d+")
PROPERTY_REGEX = re.compile(r"(Property|WikibaseProperty):P\d+")


# pylint: disable=too-many-branches,too-many-statements
def compile_log_type(record: dict) -> WikibaseLogType:
    """Compile Log Type"""

    log_type: Optional[WikibaseLogType] = None
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
        case ("approval", "approve"):
            log_type = WikibaseLogType.APPROVE
        case ("comments", "add"):
            log_type = WikibaseLogType.COMMENTS_CREATE
        case ("comments", "delete"):
            log_type = WikibaseLogType.COMMENTS_DELETE
        case ("mwoauthconsumer", "approve"):
            log_type = WikibaseLogType.CONSUMER_APPROVE
        case ("mwoauthconsumer", "create-owner-only"):
            log_type = WikibaseLogType.CONSUMER_CREATE
        case ("mwoauthconsumer", "disable"):
            log_type = WikibaseLogType.CONSUMER_DISABLE
        case ("mwoauthconsumer", "propose"):
            log_type = WikibaseLogType.CONSUMER_PROPOSE
        case ("mwoauthconsumer", "reject"):
            log_type = WikibaseLogType.CONSUMER_REJECT
        case ("mwoauthconsumer", "update"):
            log_type = WikibaseLogType.CONSUMER_UPDATE
        case ("contentmodel", "change"):
            if "oldmodel" in record["params"] and "newmodel" in record["params"]:
                log_type = WikibaseLogType.CONTENT_MODEL_CHANGE
        case ("contentmodel", "new"):
            if "oldmodel" in record["params"] and "newmodel" in record["params"]:
                log_type = WikibaseLogType.CONTENT_MODEL_CREATE
        case ("datadump", "delete"):
            log_type = WikibaseLogType.DATADUMP_DELETE
        case ("datadump", "generate"):
            log_type = WikibaseLogType.DATADUMP_GENERATE
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
        case ("html2wiki", "import"):
            log_type = WikibaseLogType.IMPORT_HTML
        case ("interwiki", "iw_add"):
            log_type = WikibaseLogType.INTERWIKI_CREATE
        case ("interwiki", "iw_delete"):
            log_type = WikibaseLogType.INTERWIKI_DELETE
        case ("interwiki", "iw_edit"):
            log_type = WikibaseLogType.INTERWIKI_EDIT
        case ("approval", "approvefile"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_APPROVE
        case ("upload", "overwrite"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_OVERWRITE
        case ("upload", "revert"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_REVERT
        case ("upload", "upload"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_UPLOAD
        case ("move", "move"):
            log_type = WikibaseLogType.MOVE
        case ("pagetranslation", "prioritylanguages"):
            if "languages" in record["params"]:
                log_type = WikibaseLogType.PAGE_TRANSLATE
        case ("pagetranslation", "deletefok"):
            log_type = WikibaseLogType.PAGE_TRANSLATE_DELETE_FOK
        case ("pagetranslation", "deletelok"):
            log_type = WikibaseLogType.PAGE_TRANSLATE_DELETE_LOK
        case ("pagetranslation", "mark"):
            log_type = WikibaseLogType.PAGE_TRANSLATE_MARK
        case ("pagetranslation", "unmark"):
            log_type = WikibaseLogType.PAGE_TRANSLATE_UNMARK
        case ("pagelang", "pagelang"):
            if "oldlanguage" in record["params"] and "newlanguage" in record["params"]:
                log_type = WikibaseLogType.PAGE_UPDATE_LANGUAGE
        case ("patrol", "autopatrol"):
            log_type = WikibaseLogType.PATROL_AUTO
        case ("patrol", "patrol"):
            log_type = WikibaseLogType.PATROL
        case ("profile", "profile"):
            log_type = WikibaseLogType.PROFILE
        case ("protect", "move_prot") | ("protect", "protect") | ("protect", "modify"):
            log_type = WikibaseLogType.PROTECT
        case ("delete", "delete_redir"):
            log_type = WikibaseLogType.REDIRECT_DELETE
        case ("move", "move_redir"):
            log_type = WikibaseLogType.REDIRECT_MOVE
        case ("delete", "revision"):
            log_type = WikibaseLogType.REVISION_DELETE
        case ("cargo", "createtable"):
            log_type = WikibaseLogType.TABLE_CREATE
        case ("cargo", "deletetable"):
            log_type = WikibaseLogType.TABLE_DELETE
        case ("managetags", "create"):
            log_type = WikibaseLogType.TAG_CREATE
        case ("thanks", "thank"):
            log_type = WikibaseLogType.THANK
        case ("approval", "unapprove"):
            log_type = WikibaseLogType.UNAPPROVE
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
        case ("managewiki", "delete-group"):
            log_type = WikibaseLogType.WIKI_GROUP_DELETE
        case ("managewiki", "namespaces"):
            log_type = WikibaseLogType.WIKI_NAMESPACES
        case ("managewiki", "rights"):
            log_type = WikibaseLogType.WIKI_RIGHTS
        case ("managewiki", "settings"):
            log_type = WikibaseLogType.WIKI_SETTINGS
    try:
        assert log_type is not None
    except AssertionError as exc:
        raise NotImplementedError(record) from exc
    return log_type
