"""Add Categories to Test Data"""

import pytest

from data import get_async_session
from model.database import WikibaseCategoryModel
from model.enum import WikibaseCategory


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="add-test-categories")
async def test_add_software():
    """Add Categories to Test Data"""

    async with get_async_session() as async_session:
        async_session.add(
            WikibaseCategoryModel(
                id=1, category=WikibaseCategory.CULTURAL_AND_HISTORICAL
            )
        )
        async_session.add(
            WikibaseCategoryModel(
                id=2, category=WikibaseCategory.DIGITAL_COLLECTIONS_AND_ARCHIVES
            )
        )
        async_session.add(
            WikibaseCategoryModel(
                id=3, category=WikibaseCategory.EDUCATIONAL_AND_REFERENCE_COLLECTIONS
            )
        )
        async_session.add(
            WikibaseCategoryModel(
                id=4, category=WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
            )
        )
        async_session.add(
            WikibaseCategoryModel(
                id=5, category=WikibaseCategory.FICTIONAL_AND_CREATIVE_WORKS
            )
        )
        async_session.add(
            WikibaseCategoryModel(id=6, category=WikibaseCategory.LEGAL_AND_POLITICAL)
        )
        async_session.add(
            WikibaseCategoryModel(
                id=7, category=WikibaseCategory.LINGUISTIC_AND_LITERARY
            )
        )
        async_session.add(
            WikibaseCategoryModel(
                id=8, category=WikibaseCategory.MATHEMATICS_AND_SCIENCE
            )
        )
        async_session.add(
            WikibaseCategoryModel(
                id=9, category=WikibaseCategory.SEMANTIC_AND_PROSOPOGRAPHIC_DATA
            )
        )
        async_session.add(
            WikibaseCategoryModel(id=10, category=WikibaseCategory.SOCIAL_AND_ADVOCACY)
        )
        async_session.add(
            WikibaseCategoryModel(
                id=11, category=WikibaseCategory.TECHNOLOGY_AND_OPEN_SOURCE
            )
        )
        await async_session.commit()
