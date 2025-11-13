"""Get Wikibase"""

from sqlalchemy import select

from data import get_async_session
from model.database import WikibaseModel
from model.strawberry.output import WikibaseStrawberryModel


async def get_wikibase(wikibase_id: int) -> WikibaseStrawberryModel:
    """Get Wikibase"""

    async with get_async_session() as async_session:
        result = (
            await async_session.scalars(
                select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
            )
        ).one()
        return WikibaseStrawberryModel.marshal(result)
