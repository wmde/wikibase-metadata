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
):  # pylint: disable=too-many-arguments
    """Assert Quantity Observation"""

    assert_property_value(returned_quantity, "id", expected_id)
    assert "observationDate" in returned_quantity
    assert_property_value(returned_quantity, "returnedData", expected_returned_data)
    assert_property_value(returned_quantity, "totalItems", expected_items)
    assert_property_value(returned_quantity, "totalLexemes", expected_lexemes)
    assert_property_value(returned_quantity, "totalProperties", expected_properties)
    assert_property_value(returned_quantity, "totalTriples", expected_triples)
