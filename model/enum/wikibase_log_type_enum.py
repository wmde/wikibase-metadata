"""Wikibase Log Type Enum"""

import enum
import re


class WikibaseLogType(enum.Enum):
    """Wikibase Log Type"""

    ABUSE_FILTER_CREATE = 1
    ABUSE_FILTER_MODIFIY = 2
    APPROVE = 3
    COMMENTS_CREATE = 4
    COMMENTS_DELETE = 5
    CONSUMER_APPROVE = 6
    CONSUMER_CREATE = 7
    CONSUMER_PROPOSE = 8
    CONSUMER_REJECT = 9
    CONSUMER_UPDATE = 10
    EVENT_DELETE = 11
    EXPORT_PDF = 12
    FEEDBACK_CREATE = 13
    FEEDBACK_FEATURE = 14
    FEEDBACK_FLAG = 15
    FEEDBACK_FLAG_INAPPROPRIATE = 16
    FEEDBACK_HIDE = 17
    FEEDBACK_NO_ACTION = 18
    FEEDBACK_RESOLVE = 19
    IMPORT = 20
    INTERWIKI_CREATE = 21
    INTERWIKI_DELETE = 22
    INTERWIKI_EDIT = 23
    ITEM_CREATE = 24
    ITEM_DELETE = 25
    MEDIA_APPROVE = 26
    MEDIA_OVERWRITE = 27
    MEDIA_REVERT = 28
    MEDIA_UPLOAD = 29
    MOVE = 30
    PAGE_CREATE = 31
    PAGE_DELETE = 32
    PAGE_TRANSLATE = 33
    PAGE_TRANSLATE_DELETE_FOK = 34
    PAGE_TRANSLATE_DELETE_LOK = 35
    PAGE_TRANSLATE_MARK = 36
    PAGE_TRANSLATE_UNMARK = 37
    PAGE_UPDATE_LANGUAGE=38
    PATROL = 39
    PATROL_AUTO = 40
    PROFILE = 41
    PROPERTY_CREATE = 42
    PROPERTY_DELETE = 43
    PROTECT = 44
    REDIRECT_DELETE = 45
    REDIRECT_MOVE = 46
    REVISION_DELETE = 47
    TAG_CREATE = 48
    UNAPPROVE = 49
    UNDO_DELETE = 50
    UNPROTECT = 51
    USER_BLOCK = 52
    USER_UNBLOCK = 53
    USER_CREATE = 54
    USER_DELETE = 55
    USER_MERGE = 56
    USER_RENAME = 57
    USER_RIGHTS = 58
    WIKI_FARM = 59
    WIKI_NAMESPACES = 60
    WIKI_RIGHTS = 61
    WIKI_SETTINGS = 62


MEDIA_REGEX = re.compile(r".*\.(flv|gif|jpg|pdf|png)", re.IGNORECASE)
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
        case ("approval", "approvefile"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_APPROVE
            else:
                raise NotImplementedError(record)
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
        case ("pagetranslation", "prioritylanguages"):
            if 'languages' in record['params']:
                log_type = WikibaseLogType.PAGE_TRANSLATE
            else:
                raise NotImplementedError(record)
        case ("pagetranslation", "deletefok"):
                log_type = WikibaseLogType.PAGE_TRANSLATE_DELETE_FOK
        case ("pagetranslation", "deletelok"):
                log_type = WikibaseLogType.PAGE_TRANSLATE_DELETE_LOK
        case ("pagetranslation", "mark"):
                log_type = WikibaseLogType.PAGE_TRANSLATE_MARK
        case ("pagetranslation", "unmark"):
                log_type = WikibaseLogType.PAGE_TRANSLATE_UNMARK
        case ("pagelang", "pagelang"):
                if 'oldlanguage' in record["params"] and 'newlanguage' in record["params"]:
                    log_type = WikibaseLogType.PAGE_UPDATE_LANGUAGE
                else:
                    raise NotImplementedError(record)
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
        case ("managetags", "create"):
            log_type = WikibaseLogType.TAG_CREATE
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
        case ("managewiki", "namespaces"):
            log_type = WikibaseLogType.WIKI_NAMESPACES
        case ("managewiki", "rights"):
            log_type = WikibaseLogType.WIKI_RIGHTS
        case ("managewiki", "settings"):
            log_type = WikibaseLogType.WIKI_SETTINGS
        case _:
            raise NotImplementedError(record)
    return log_type
