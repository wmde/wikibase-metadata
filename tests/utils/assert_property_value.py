"""Test Utilities"""

from typing import List


def assert_property_value(data: dict, prop: str, expected_value: any):
    """Assert property has value"""
    assert prop in data, f"{prop} not found in {data.keys()}"
    assert (
        actual := data[prop]
    ) == expected_value, (
        f"Expected {prop} to be {expected_value}, Actual {actual}; ({data})"
    )


def assert_layered_property_count(data: dict, props: list[str], expected_count: int):
    """Assert property has value levels deep"""
    if len(props) == 0:
        assert (
            len(data) == expected_count
        ), f"Expected length {expected_count}, actual {len(data)}"
    else:
        prop = props.pop(0)
        if isinstance(prop, str):
            assert prop in data, f"{prop} not found in {data.keys()}"
        else:
            assert isinstance(data, List)
            assert len(data) >= prop
        assert data[prop] is not None
        assert_layered_property_count(data[prop], props, expected_count)


def assert_layered_property_value(
    data: dict, props: list[int | str], expected_value: any
):
    """Assert property has value levels deep"""
    if len(props) < 1:
        raise ValueError(f"Props must have at least one value: {props}")
    if len(props) == 1:
        assert_property_value(data, props.pop(), expected_value)
    else:
        prop = props.pop(0)
        if isinstance(prop, str):
            assert prop in data, f"{prop} not found in {data.keys()}"
        else:
            assert isinstance(data, List)
            assert len(data) >= prop
        assert data[prop] is not None
        assert_layered_property_value(data[prop], props, expected_value)
