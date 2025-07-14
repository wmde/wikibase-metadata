"""Test Join URL"""

from model.database.wikibase_url_model import join_url


def test_join_url():
    """Test join_url"""

    assert join_url("https://ao3.org", "Special:Page") == "https://ao3.org/Special:Page"
    assert (
        join_url("https://ao3.org", "", "Special:Page")
        == "https://ao3.org/Special:Page"
    )
    assert (
        join_url("https://ao3.org/", "/", "Special:Page")
        == "https://ao3.org/Special:Page"
    )
    assert (
        join_url("https://ao3.org/", "/wiki/", "Special:Page")
        == "https://ao3.org/wiki/Special:Page"
    )
