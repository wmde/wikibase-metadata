"""Update Wikibase opt-in status"""

from sqlalchemy import select

from data.database_connection import get_async_session
from model.database import WikibaseModel
from resolvers.add.add_wikibase import clear_optional_wikibase_data


async def update_wikibase_opt_in(wikibase_id: int, opt_in: bool) -> bool:
    """Update Wikibase opt-in status."""

    async with get_async_session() as async_session:
        model = await async_session.scalar(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )

        if model is None:
            return False

        model.opt_in = opt_in

        if not opt_in:
            await clear_optional_wikibase_data(async_session, model)
        else:
            model.checked = True

        await async_session.commit()

        return True
