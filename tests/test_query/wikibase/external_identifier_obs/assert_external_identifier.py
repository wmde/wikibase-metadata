"""Assert External Identifier Observation"""

from tests.utils import assert_property_value


# pylint: disable-next=too-many-arguments,too-many-positional-arguments
def assert_external_identifier(
    returned_ei_data: dict,
    expected_id: str,
    expected_returned_data: bool,
    expected_external_identifier_properties: int,
    expected_external_identifier_statements: int,
    expected_url_properties: int,
    expected_url_statements: int,
):
    """Assert External Identifier Observation"""

    assert_property_value(returned_ei_data, "id", expected_id)
    assert "observationDate" in returned_ei_data
    assert_property_value(returned_ei_data, "returnedData", expected_returned_data)
    assert_property_value(
        returned_ei_data,
        "totalExternalIdentifierProperties",
        expected_external_identifier_properties,
    )
    assert_property_value(
        returned_ei_data,
        "totalExternalIdentifierStatements",
        expected_external_identifier_statements,
    )
    assert_property_value(
        returned_ei_data, "totalUrlProperties", expected_url_properties
    )
    assert_property_value(
        returned_ei_data, "totalUrlStatements", expected_url_statements
    )
