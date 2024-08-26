"""Wikibase Log Type Enum"""

import enum
import re
from typing import Optional


class WikibaseLogType(enum.Enum):
    """Wikibase Log Type"""

    ABUSE_FILTER_CREATE = 1
    ABUSE_FILTER_MODIFIY = 2
    ACHIEVEMENT_BADGE = 3
    APPROVE = 4
    COMMENTS_CREATE = 5
    COMMENTS_DELETE = 6
    CONSUMER_APPROVE = 7
    CONSUMER_CREATE = 8
    CONSUMER_DISABLE = 9
    CONSUMER_PROPOSE = 10
    CONSUMER_REJECT = 11
    CONSUMER_UPDATE = 12
    CONFIG_UPDATE = 13
    CONTENT_MODEL_CREATE = 14
    CONTENT_MODEL_CHANGE = 15
    DATADUMP_DELETE = 16
    DATADUMP_GENERATE = 17
    EVENT_DELETE = 18
    EXPORT_PDF = 19
    FEEDBACK_CREATE = 20
    FEEDBACK_FEATURE = 21
    FEEDBACK_FLAG = 22
    FEEDBACK_FLAG_INAPPROPRIATE = 23
    FEEDBACK_HIDE = 24
    FEEDBACK_NO_ACTION = 25
    FEEDBACK_RESOLVE = 26
    IMPORT = 27
    IMPORT_HTML = 28
    INTERWIKI_CREATE = 29
    INTERWIKI_DELETE = 30
    INTERWIKI_EDIT = 31
    ITEM_CREATE = 32
    ITEM_DELETE = 33
    LOCK_FLOW_LOCK_TOPIC = 34
    MEDIA_APPROVE = 35
    MEDIA_OVERWRITE = 36
    MEDIA_REVERT = 37
    MEDIA_UPLOAD = 38
    MOVE = 39
    PAGE_CREATE = 40
    PAGE_DELETE = 41
    PAGE_TRANSLATE = 42
    PAGE_TRANSLATE_DELETE_FOK = 43
    PAGE_TRANSLATE_DELETE_LOK = 44
    PAGE_TRANSLATE_MARK = 45
    PAGE_TRANSLATE_UNMARK = 46
    PAGE_UPDATE_LANGUAGE = 47
    PATROL = 48
    PATROL_AUTO = 49
    PROFILE = 50
    PROPERTY_CREATE = 51
    PROPERTY_DELETE = 52
    PROTECT = 53
    REDIRECT_DELETE = 54
    REDIRECT_MOVE = 55
    REVISION_DELETE = 56
    TABLE_CREATE = 57
    TABLE_DELETE = 58
    TAG_CREATE = 59
    THANK = 60
    UNAPPROVE = 61
    UNDO_DELETE = 62
    UNPROTECT = 63
    USER_BLOCK = 64
    USER_UNBLOCK = 65
    USER_CREATE = 66
    USER_DELETE = 67
    USER_MERGE = 68
    USER_RENAME = 69
    USER_RIGHTS = 70
    WIKI_FARM = 71
    WIKI_GROUP_DELETE = 72
    WIKI_NAMESPACES = 73
    WIKI_RIGHTS = 74
    WIKI_SETTINGS = 75


MEDIA_REGEX = re.compile(r".*\.(flv|gif|jpe?g|pdf|png|svg|wav|webm)", re.IGNORECASE)
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
        case (
            ("achievementbadges", "be-thanked")
            | ("achievementbadges", "contribs-sunday")
            | ("achievementbadges", "contribs-monday")
            | ("achievementbadges", "contribs-tuesday")
            | ("achievementbadges", "contribs-thursday")
            | ("achievementbadges", "contribs-friday")
            | ("achievementbadges", "contribs-saturday")
            | ("achievementbadges", "create-page")
            | ("achievementbadges", "edit-page")
            | ("achievementbadges", "edit-size")
            | ("achievementbadges", "long-user-page")
            | ("achievementbadges", "sign-up")
            | ("achievementbadges", "thanks")
            | ("achievementbadges", "visual-edit")
        ):
            log_type = WikibaseLogType.ACHIEVEMENT_BADGE
        case ("approval", "approve"):
            log_type = WikibaseLogType.APPROVE
        case ("comments", "add"):
            log_type = WikibaseLogType.COMMENTS_CREATE
        case ("comments", "delete"):
            log_type = WikibaseLogType.COMMENTS_DELETE
        case ("stable", "config"):
            log_type = WikibaseLogType.CONFIG_UPDATE
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
            else:
                pass
        case ("contentmodel", "new"):
            if "oldmodel" in record["params"] and "newmodel" in record["params"]:
                log_type = WikibaseLogType.CONTENT_MODEL_CREATE
            else:
                pass
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
        case ("lock", "flow-lock-topic"):
            log_type = WikibaseLogType.LOCK_FLOW_LOCK_TOPIC
        case ("approval", "approvefile"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_APPROVE
            else:
                pass
        case ("upload", "overwrite"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_OVERWRITE
            else:
                pass
        case ("upload", "revert"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_REVERT
            else:
                pass
        case ("upload", "upload") | ("remoteupload", "file"):
            if "img_sha1" in record["params"] or MEDIA_REGEX.match(record["title"]):
                log_type = WikibaseLogType.MEDIA_UPLOAD
            else:
                pass
        case ("remoteupload", "stashedfile"):
            if "remotetitle" in record["params"]:
                if MEDIA_REGEX.match(record["params"]["remotetitle"]):
                    log_type = WikibaseLogType.MEDIA_UPLOAD
                else:
                    pass
            else:
                pass
        case ("move", "move"):
            log_type = WikibaseLogType.MOVE
        case ("pagetranslation", "prioritylanguages"):
            if "languages" in record["params"]:
                log_type = WikibaseLogType.PAGE_TRANSLATE
            else:
                pass
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
            else:
                pass
        case ("patrol", "patrol"):
            log_type = WikibaseLogType.PATROL
        case ("patrol", "autopatrol"):
            log_type = WikibaseLogType.PATROL_AUTO
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
        case ("renameuser", "renameuser"):
            log_type = WikibaseLogType.USER_RENAME
        case ("rights", "rights") | ("rights", "blockautopromote"):
            log_type = WikibaseLogType.USER_RIGHTS
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
