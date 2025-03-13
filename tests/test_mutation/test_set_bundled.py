"""Test Merge Software"""

import pytest

from tests.test_schema import test_schema


BUNDLE_SOFTWARE_QUERY = """
mutation MyMutation($extensionId: Int!, $bundled: Boolean) {
  setExtensionWbsBundled(extensionId: $extensionId, bundled: $bundled)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="test-set-bundled")
async def test_set_bundled():
    """Test Set Extension Bundled"""

    result = await test_schema.execute(
        BUNDLE_SOFTWARE_QUERY, variable_values={"extensionId": 2}
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("setExtensionWbsBundled")


# @pytest.mark.asyncio
# @pytest.mark.mutation
# @pytest.mark.dependency(name="merge-software-by-id-fail-same-id")
# async def test_merge_software_by_id_mutation_fail_same_id():
#     """Test Merge Software by ID - Same IDs"""

#     result = await test_schema.execute(
#         BUNDLE_SOFTWARE_QUERY, variable_values={"baseId": 1, "additionalId": 1}
#     )
#     assert result.errors is not None
#     assert result.errors[0].message == "Software IDs Must Be Distinct"


# @pytest.mark.asyncio
# @pytest.mark.mutation
# @pytest.mark.dependency(name="merge-software-by-id-fail-not-found")
# async def test_merge_software_by_id_mutation_fail_not_found():
#     """Test Merge Software by ID - Not Found"""

#     result = await test_schema.execute(
#         BUNDLE_SOFTWARE_QUERY, variable_values={"baseId": 1, "additionalId": 1000000}
#     )
#     assert result.errors is not None
#     assert result.errors[0].message == "1 Record Found, 2 Needed to Merge"


# @pytest.mark.asyncio
# @pytest.mark.mutation
# @pytest.mark.dependency(
#     depends=["software-version-success"],
#     name="merge-software-by-id-fail-different-types",
#     scope="session",
# )
# async def test_merge_software_by_id_mutation_fail_different_types():
#     """Test Add Wikibase"""

#     result = await test_schema.execute(
#         BUNDLE_SOFTWARE_QUERY, variable_values={"baseId": 1, "additionalId": 4}
#     )
#     assert result.errors is not None
#     assert result.errors[0].message == "Cannot Merge Differently-Typed Software"
