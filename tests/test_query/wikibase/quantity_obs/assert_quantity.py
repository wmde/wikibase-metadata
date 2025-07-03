"""Assert Quantity Observation"""

from tests.utils import assert_property_value


def assert_quantity(
    returned_quantity: dict,
    expected_id: str,
    expected_returned_data: bool,
    expected_items: int,
    expected_lexemes: int,
    expected_properties: int,
    expected_triples: int,
    expected_external_identifier_properties: int,
    expected_external_identifier_statements: int,
    expected_url_properties: int,
    expected_url_statements: int,
):
    """Assert Quantity Observation"""

    assert_property_value(returned_quantity, "id", expected_id)
    assert "observationDate" in returned_quantity
    assert_property_value(returned_quantity, "returnedData", expected_returned_data)
    assert_property_value(returned_quantity, "totalItems", expected_items)
    assert_property_value(returned_quantity, "totalLexemes", expected_lexemes)
    assert_property_value(returned_quantity, "totalProperties", expected_properties)
    assert_property_value(returned_quantity, "totalTriples", expected_triples)
    assert_property_value(
        returned_quantity,
        "totalExternalIdentifierProperties",
        expected_external_identifier_properties,
    )
    assert_property_value(
        returned_quantity,
        "totalExternalIdentifierStatements",
        expected_external_identifier_statements,
    )
    assert_property_value(
        returned_quantity, "totalUrlProperties", expected_url_properties
    )
    assert_property_value(
        returned_quantity, "totalUrlStatements", expected_url_statements
    )
