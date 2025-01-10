"""Merge Software"""

from sqlalchemy import and_, delete, select, update
from data.database_connection import get_async_session
from model.database import (
    WikibaseSoftwareVersionModel,
)
from model.database import WikibaseSoftwareModel
from model.database.wikibase_software.software_tag_xref_model import (
    software_tag_xref_table,
)


async def merge_software_by_id(base_id: int, additional_id: int) -> int:
    """Merge Software by ID"""

    async with get_async_session() as async_session:
        software_query = select(WikibaseSoftwareModel.software_type).where(
            WikibaseSoftwareModel.id.in_([base_id, additional_id])
        )
        software_type_list = (await async_session.scalars(software_query)).all()
        assert len({software_type_list}) == 1

        update_software_version_query = (
            update(WikibaseSoftwareVersionModel)
            .where(WikibaseSoftwareVersionModel.software_id == additional_id)
            .values(software_id=base_id)
        )
        await async_session.execute(update_software_version_query)

        update_software_tags_query = software_tag_xref_table.insert().from_select(
            [
                software_tag_xref_table.c.wikibase_software_id,
                software_tag_xref_table.c.wikibase_software_tag_id,
            ],
            select(
                software_tag_xref_table.c.wikibase_software_id,
                software_tag_xref_table.c.wikibase_software_tag_id,
            ).where(
                and_(
                    software_tag_xref_table.c.wikibase_software_id == additional_id,
                    software_tag_xref_table.c.wikibase_software_tag_id.not_in(
                        select(
                            software_tag_xref_table.c.wikibase_software_tag_id
                        ).where(
                            software_tag_xref_table.c.wikibase_software_id == base_id
                        )
                    ),
                )
            ),
        )
        await async_session.execute(update_software_tags_query)

        delete_additional_tags_query = software_tag_xref_table.delete().where(
            software_tag_xref_table.c.wikibase_software_id == additional_id
        )
        await async_session.execute(delete_additional_tags_query)

        await async_session.flush()

        delete_software_query = delete(WikibaseSoftwareModel).where(
            WikibaseSoftwareModel.id == additional_id
        )
        await async_session.execute(delete_software_query)

        await async_session.commit()

    return 1
