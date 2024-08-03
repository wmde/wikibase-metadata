"""Test Utilities"""


def assert_property_value(data: dict, prop: str, expected_value: any):
    """Assert property has value"""
    assert prop in data, f"{prop} not found in {data.keys()}"
    assert (
        actual := data[prop]
    ) == expected_value, f"Expected {expected_value}, Actual {actual}"


def assert_layered_property_value(data: dict, props: list[str], expected_value: any):
    """Assert property has value levels deep"""
    if len(props) < 1:
        raise ValueError(f"Props must have at least one value: {props}")
    if len(props) == 1:
        assert_property_value(data, props.pop(), expected_value)
    else:
        prop = props.pop(0)
        assert prop in data, f"{prop} not found in {data.keys()}"
        assert data[prop] is not None
        assert_layered_property_value(data[prop], props, expected_value)
