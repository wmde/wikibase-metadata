"""Get or Create Software Model"""

import re
from typing import Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from model.database import WikibaseSoftwareModel
from model.enum import WikibaseSoftwareType

EXTENSIONNAME_PATTERN = r"⧼([a-z]+)-extensionname⧽"


async def get_or_create_software_model(
    async_session: AsyncSession, software_type: WikibaseSoftwareType, software_name: str
) -> WikibaseSoftwareModel:
    """Fetch or Create Software Model"""

    if re.match(EXTENSIONNAME_PATTERN, software_name):
        software_name = re.sub(EXTENSIONNAME_PATTERN, r"\1", software_name)

    existing = (
        await async_session.scalars(
            select(WikibaseSoftwareModel).where(
                and_(
                    WikibaseSoftwareModel.software_type == software_type,
                    WikibaseSoftwareModel.software_name == software_name,
                )
            )
        )
    ).one_or_none()
    if existing is not None:
        return existing

    all_software_of_type = (
        await async_session.scalars(
            select(WikibaseSoftwareModel).where(
                WikibaseSoftwareModel.software_type == software_type,
            )
        )
    ).all()
    nearby: Optional[WikibaseSoftwareModel] = None
    nearby_count = 0
    for s in all_software_of_type:
        if (
            s.software_name.replace(" ", "").lower()
            == software_name.replace(" ", "").lower()
        ):
            nearby = s
            nearby_count += 1
    assert nearby_count <= 1
    if nearby is not None:
        return nearby

    creating = WikibaseSoftwareModel(
        software_type=software_type, software_name=software_name
    )
    async_session.add(creating)
    await async_session.flush()
    await async_session.refresh(creating)
    return creating
