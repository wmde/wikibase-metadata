"""Test compile log type"""

import pytest
from model.enum import WikibaseLogType, compile_log_type


@pytest.mark.log
@pytest.mark.parametrize(
    ["log_type", "action", "title", "params", "expected_result"],
    [
        ("create", "create", "Item:Q1", {}, WikibaseLogType.ITEM_CREATE),
        ("create", "create", "Property:P1", {}, WikibaseLogType.PROPERTY_CREATE),
        ("create", "create", "Test Page", {}, WikibaseLogType.PAGE_CREATE),
        ("delete", "delete", "Item:Q1", {}, WikibaseLogType.ITEM_DELETE),
        ("delete", "delete", "Property:P1", {}, WikibaseLogType.PROPERTY_DELETE),
        ("delete", "delete", "Former Test Page", {}, WikibaseLogType.PAGE_DELETE),
        ("abusefilter", "create", "", {}, WikibaseLogType.ABUSE_FILTER_CREATE),
        ("abusefilter", "modify", "", {}, WikibaseLogType.ABUSE_FILTER_MODIFIY),
        ("achievementbadges", "be-thanked", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        (
            "achievementbadges",
            "contribs-sunday",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        (
            "achievementbadges",
            "contribs-monday",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        (
            "achievementbadges",
            "contribs-tuesday",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        (
            "achievementbadges",
            "contribs-thursday",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        (
            "achievementbadges",
            "contribs-friday",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        (
            "achievementbadges",
            "contribs-saturday",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        ("achievementbadges", "create-page", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        ("achievementbadges", "edit-page", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        ("achievementbadges", "edit-size", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        (
            "achievementbadges",
            "long-user-page",
            "",
            {},
            WikibaseLogType.ACHIEVEMENT_BADGE,
        ),
        ("achievementbadges", "sign-up", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        ("achievementbadges", "thanks", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        ("achievementbadges", "visual-edit", "", {}, WikibaseLogType.ACHIEVEMENT_BADGE),
        ("approval", "approve", "", {}, WikibaseLogType.APPROVE),
        ("comments", "add", "", {}, WikibaseLogType.COMMENTS_CREATE),
        ("comments", "delete", "", {}, WikibaseLogType.COMMENTS_DELETE),
        ("stable", "config", "", {}, WikibaseLogType.CONFIG_UPDATE),
        ("mwoauthconsumer", "approve", "", {}, WikibaseLogType.CONSUMER_APPROVE),
        (
            "mwoauthconsumer",
            "create-owner-only",
            "",
            {},
            WikibaseLogType.CONSUMER_CREATE,
        ),
        ("mwoauthconsumer", "disable", "", {}, WikibaseLogType.CONSUMER_DISABLE),
        ("mwoauthconsumer", "propose", "", {}, WikibaseLogType.CONSUMER_PROPOSE),
        ("mwoauthconsumer", "reject", "", {}, WikibaseLogType.CONSUMER_REJECT),
        ("mwoauthconsumer", "update", "", {}, WikibaseLogType.CONSUMER_UPDATE),
        (
            "contentmodel",
            "change",
            "",
            {"oldmodel": "a", "newmodel": "b"},
            WikibaseLogType.CONTENT_MODEL_CHANGE,
        ),
        (
            "contentmodel",
            "new",
            "",
            {"oldmodel": "a", "newmodel": "b"},
            WikibaseLogType.CONTENT_MODEL_CREATE,
        ),
        ("datadump", "delete", "", {}, WikibaseLogType.DATADUMP_DELETE),
        ("datadump", "generate", "", {}, WikibaseLogType.DATADUMP_GENERATE),
        ("delete", "event", "", {}, WikibaseLogType.EVENT_DELETE),
        ("pdf", "book", "", {}, WikibaseLogType.EXPORT_PDF),
        ("articlefeedbackv5", "create", "", {}, WikibaseLogType.FEEDBACK_CREATE),
        ("articlefeedbackv5", "feature", "", {}, WikibaseLogType.FEEDBACK_FEATURE),
        ("articlefeedbackv5", "flag", "", {}, WikibaseLogType.FEEDBACK_FLAG),
        (
            "articlefeedbackv5",
            "inappropriate",
            "",
            {},
            WikibaseLogType.FEEDBACK_FLAG_INAPPROPRIATE,
        ),
        ("articlefeedbackv5", "hide", "", {}, WikibaseLogType.FEEDBACK_HIDE),
        ("articlefeedbackv5", "noaction", "", {}, WikibaseLogType.FEEDBACK_NO_ACTION),
        ("articlefeedbackv5", "resolve", "", {}, WikibaseLogType.FEEDBACK_RESOLVE),
        ("import", "upload", "", {}, WikibaseLogType.IMPORT),
        ("html2wiki", "import", "", {}, WikibaseLogType.IMPORT_HTML),
        ("interwiki", "iw_add", "", {}, WikibaseLogType.INTERWIKI_CREATE),
        ("interwiki", "iw_delete", "", {}, WikibaseLogType.INTERWIKI_DELETE),
        ("interwiki", "iw_edit", "", {}, WikibaseLogType.INTERWIKI_EDIT),
        ("lock", "flow-lock-topic", "", {}, WikibaseLogType.LOCK_FLOW_LOCK_TOPIC),
        ("approval", "approvefile", "slides.pdf", {}, WikibaseLogType.MEDIA_APPROVE),
        (
            "approval",
            "approvefile",
            "",
            {"img_sha1": ""},
            WikibaseLogType.MEDIA_APPROVE,
        ),
        ("upload", "overwrite", "slides.pdf", {}, WikibaseLogType.MEDIA_OVERWRITE),
        ("upload", "overwrite", "", {"img_sha1": ""}, WikibaseLogType.MEDIA_OVERWRITE),
        ("upload", "revert", "slides.pdf", {}, WikibaseLogType.MEDIA_REVERT),
        ("upload", "revert", "", {"img_sha1": ""}, WikibaseLogType.MEDIA_REVERT),
        ("upload", "upload", "slides.pdf", {}, WikibaseLogType.MEDIA_UPLOAD),
        ("upload", "upload", "", {"img_sha1": ""}, WikibaseLogType.MEDIA_UPLOAD),
        ("remoteupload", "file", "slides.pdf", {}, WikibaseLogType.MEDIA_UPLOAD),
        ("remoteupload", "file", "", {"img_sha1": ""}, WikibaseLogType.MEDIA_UPLOAD),
        (
            "remoteupload",
            "stashedfile",
            "",
            {"remotetitle": "slides.pdf"},
            WikibaseLogType.MEDIA_UPLOAD,
        ),
        ("move", "move", "", {}, WikibaseLogType.MOVE),
        (
            "pagetranslation",
            "prioritylanguages",
            "",
            {"languages": "eng"},
            WikibaseLogType.PAGE_TRANSLATE,
        ),
        (
            "pagetranslation",
            "deletefok",
            "",
            {},
            WikibaseLogType.PAGE_TRANSLATE_DELETE_FOK,
        ),
        (
            "pagetranslation",
            "deletelok",
            "",
            {},
            WikibaseLogType.PAGE_TRANSLATE_DELETE_LOK,
        ),
        ("pagetranslation", "mark", "", {}, WikibaseLogType.PAGE_TRANSLATE_MARK),
        ("pagetranslation", "unmark", "", {}, WikibaseLogType.PAGE_TRANSLATE_UNMARK),
        (
            "pagelang",
            "pagelang",
            "",
            {"oldlanguage": "eng", "newlanguage": "de"},
            WikibaseLogType.PAGE_UPDATE_LANGUAGE,
        ),
        ("patrol", "autopatrol", "", {}, WikibaseLogType.PATROL_AUTO),
        ("patrol", "patrol", "", {}, WikibaseLogType.PATROL),
        ("profile", "profile", "", {}, WikibaseLogType.PROFILE),
        ("protect", "move_prot", "", {}, WikibaseLogType.PROTECT),
        ("protect", "protect", "", {}, WikibaseLogType.PROTECT),
        ("protect", "modify", "", {}, WikibaseLogType.PROTECT),
        ("delete", "delete_redir", "", {}, WikibaseLogType.REDIRECT_DELETE),
        ("move", "move_redir", "", {}, WikibaseLogType.REDIRECT_MOVE),
        ("delete", "revision", "", {}, WikibaseLogType.REVISION_DELETE),
        ("cargo", "createtable", "", {}, WikibaseLogType.TABLE_CREATE),
        ("cargo", "deletetable", "", {}, WikibaseLogType.TABLE_DELETE),
        ("managetags", "create", "", {}, WikibaseLogType.TAG_CREATE),
        ("thanks", "thank", "", {}, WikibaseLogType.THANK),
        ("approval", "unapprove", "", {}, WikibaseLogType.UNAPPROVE),
        ("delete", "restore", "", {}, WikibaseLogType.UNDO_DELETE),
        ("protect", "unprotect", "", {}, WikibaseLogType.UNPROTECT),
        ("block", "block", "", {}, WikibaseLogType.USER_BLOCK),
        ("block", "reblock", "", {}, WikibaseLogType.USER_BLOCK),
        ("block", "unblock", "", {}, WikibaseLogType.USER_UNBLOCK),
        ("newusers", "autocreate", "", {}, WikibaseLogType.USER_CREATE),
        ("newusers", "byemail", "", {}, WikibaseLogType.USER_CREATE),
        ("newusers", "create", "", {}, WikibaseLogType.USER_CREATE),
        ("newusers", "create2", "", {}, WikibaseLogType.USER_CREATE),
        ("usermerge", "deleteuser", "", {}, WikibaseLogType.USER_DELETE),
        ("usermerge", "mergeuser", "", {}, WikibaseLogType.USER_MERGE),
        ("rights", "rights", "", {}, WikibaseLogType.USER_RIGHTS),
        ("rights", "blockautopromote", "", {}, WikibaseLogType.USER_RIGHTS),
        ("renameuser", "renameuser", "", {}, WikibaseLogType.USER_RENAME),
        ("farmer", "managewiki", "", {}, WikibaseLogType.WIKI_FARM),
        ("managewiki", "delete-group", "", {}, WikibaseLogType.WIKI_GROUP_DELETE),
        ("managewiki", "namespaces", "", {}, WikibaseLogType.WIKI_NAMESPACES),
        ("managewiki", "rights", "", {}, WikibaseLogType.WIKI_RIGHTS),
        ("managewiki", "settings", "", {}, WikibaseLogType.WIKI_SETTINGS),
    ],
)
def test_compile_log_type_success(
    log_type: str,
    action: str,
    title: str,
    params: dict,
    expected_result: WikibaseLogType,
):
    """Test Log Type"""

    assert (
        compile_log_type(
            {"type": log_type, "action": action, "title": title, "params": params}
        )
        == expected_result
    )


@pytest.mark.log
@pytest.mark.parametrize(
    ["log_type", "action", "title", "params"],
    [
        ("", "", "", {}),
        ("contentmodel", "change", "", {}),
        ("contentmodel", "change", "", {"oldmodel": "a"}),
        ("contentmodel", "change", "", {"newmodel": "a"}),
        ("contentmodel", "new", "", {}),
        ("contentmodel", "new", "", {"oldmodel": "a"}),
        ("contentmodel", "new", "", {"newmodel": "a"}),
        ("approval", "approvefile", "", {}),
        ("upload", "overwrite", "", {}),
        ("upload", "revert", "", {}),
        ("upload", "upload", "", {}),
        ("remoteupload", "file", "", {}),
        ("remoteupload", "stashedfile", "", {}),
        ("remoteupload", "stashedfile", "", {"remotetitle": "slides"}),
        ("pagetranslation", "prioritylanguages", "", {}),
        ("pagelang", "pagelang", "", {}),
        ("pagelang", "pagelang", "", {"oldlanguage": "a"}),
        ("pagelang", "pagelang", "", {"newlanguage": "a"}),
    ],
)
def test_compile_log_type_failure(log_type: str, action: str, title: str, params: dict):
    """Test Log Type"""

    record = {"type": log_type, "action": action, "title": title, "params": params}

    try:
        compile_log_type(record)
        assert False
    except NotImplementedError as err:
        assert str(err) == str(record)
