"""Update WBS Bundled"""

from sqlalchemy import select, update
from data.database_connection import get_async_session
from model.database import WikibaseSoftwareModel
from model.enum import WikibaseSoftwareType


async def set_extension_wbs_bundled(extension_id: int, bundled: bool = True) -> bool:
    """Set Extensions WBS Bundled"""

    async with get_async_session() as async_session:
        assert (
            await async_session.scalar(
                select(WikibaseSoftwareModel.software_type).where(
                    WikibaseSoftwareModel.id == extension_id
                )
            )
        ) == WikibaseSoftwareType.EXTENSION, "Can only update Extensions"
        await async_session.execute(
            update(WikibaseSoftwareModel)
            .where(WikibaseSoftwareModel.id == extension_id)
            .values(wikibase_suite_bundled=bundled)
        )
        await async_session.commit()

    async with get_async_session() as async_session:
        return (
            await async_session.scalar(
                select(WikibaseSoftwareModel.wikibase_suite_bundled).where(
                    WikibaseSoftwareModel.id == extension_id
                )
            )
        ) == bundled
