"""Get Wikibase List"""

from typing import List

from sqlalchemy import select

from data.database_connection import get_async_session
from model.database import WikibaseModel
from model.strawberry.output import WikibaseStrawberryModel


async def get_wikibase_list() -> List[WikibaseStrawberryModel]:
    """Get Wikibase List"""

    async with get_async_session() as async_session:
        results = (await async_session.scalars(select(WikibaseModel))).all()
        return [WikibaseStrawberryModel.marshal(c) for c in results]
