# pylint: disable=line-too-long

"""Test get_filtered_wikibase_query"""

import pytest

from model.enum import WikibaseType
from model.strawberry.input.wikibase_filter_input import (
    WikibaseFilterInput,
    WikibaseTypeInput,
)
from resolvers.util import get_filtered_wikibase_query


@pytest.mark.query
def test_get_default_query():
    """Test with no filter"""

    query = get_filtered_wikibase_query(wikibase_filter=None)
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_ignore_reuse_false():
    """Test with ignore_reuse: false"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(ignore_reuse=False)
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_ignore_reuse_true():
    """Test with ignore_reuse: true"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(ignore_reuse=True)
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_search_text_empty():
    """Test with empty search_text"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(search_text="")
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_search_text_filled():
    """Test with kosher search text"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(search_text="asdf")
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse AND (lower(wikibase.wikibase_name) LIKE lower(:wikibase_name_1) OR (EXISTS (SELECT 1
FROM wikibase_url
WHERE wikibase.id = wikibase_url.wikibase_id AND wikibase_url.url_type = :url_type_1 AND lower(wikibase_url.url) LIKE lower(:url_1))) OR (EXISTS (SELECT 1
FROM wikibase_category
WHERE wikibase_category.id = wikibase.wikibase_category_id AND CAST(wikibase_category.category AS VARCHAR) LIKE :param_1)))"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_search_text_illegal():
    """Test with non-kosher search text"""

    try:
        get_filtered_wikibase_query(
            wikibase_filter=WikibaseFilterInput(search_text='Illegal! Punctuation"",')
        )
        assert False
    except ValueError as exc:
        assert str(exc) == 'Disallowed Characters: !"",'


@pytest.mark.query
def test_get_query_type_unfilled():
    """Test with empty type input"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(wikibase_type=WikibaseTypeInput())
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_type_empty():
    """Test with empty exclude/include"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(
            wikibase_type=WikibaseTypeInput(exclude=[], include=[])
        )
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_type_exclude():
    """Test with populated exclude"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(
            wikibase_type=WikibaseTypeInput(
                exclude=[WikibaseType.CLOUD, WikibaseType.OTHER]
            )
        )
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse AND (wikibase.wb_type IS NULL OR (wikibase.wb_type NOT IN (__[POSTCOMPILE_wb_type_1])))"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())


@pytest.mark.query
def test_get_query_type_include():
    """Test with populated include"""

    query = get_filtered_wikibase_query(
        wikibase_filter=WikibaseFilterInput(
            wikibase_type=WikibaseTypeInput(
                include=[WikibaseType.CLOUD, WikibaseType.OTHER]
            )
        )
    )
    expected_query = """SELECT wikibase.id, wikibase.wikibase_name, wikibase.organization, wikibase.description, wikibase.country, wikibase.region, wikibase.wikibase_category_id, wikibase.wb_type, wikibase.valid, wikibase.test, wikibase.opt_in, wikibase.reuse, wikibase.date_added
FROM wikibase
WHERE wikibase.valid AND wikibase.reuse AND wikibase.wb_type IN (__[POSTCOMPILE_wb_type_1])"""

    assert " ".join(str(query).split()) == " ".join(expected_query.split())
