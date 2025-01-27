"""Merge Software"""

from sqlalchemy import Select, Update, and_, delete, select, update
from data.database_connection import get_async_session
from model.database import (
    WikibaseSoftwareVersionModel,
)
from model.database import WikibaseSoftwareModel
from model.database.wikibase_software.software_tag_xref_model import (
    software_tag_xref_table,
)


async def merge_software_by_id(base_id: int, additional_id: int) -> bool:
    """Merge Software by ID"""

    assert base_id != additional_id, "Software IDs Must Be Distinct"

    software_query = get_select_software_query([base_id, additional_id])
    update_software_version_query = get_update_software_version_query(
        base_id, additional_id
    )
    update_software_tags_query = get_update_software_tags_query(base_id, additional_id)
    delete_additional_tags_query = software_tag_xref_table.delete().where(
        software_tag_xref_table.c.wikibase_software_id == additional_id
    )
    delete_software_query = delete(WikibaseSoftwareModel).where(
        WikibaseSoftwareModel.id == additional_id
    )

    async with get_async_session() as async_session:
        software_list = (await async_session.scalars(software_query)).all()
        assert (
            len({s.software_type for s in software_list}) == 1
        ), "Cannot Merge Differently-Typed Software"
        assert (
            software_count := len(software_list)
        ) == 2, f"{software_count} Records Found, 2 Needed to Merge"

        await async_session.execute(update_software_version_query)
        await async_session.execute(update_software_tags_query)
        await async_session.execute(delete_additional_tags_query)
        await async_session.flush()

        await async_session.execute(delete_software_query)
        await async_session.commit()

    async with get_async_session() as async_session:
        remaining = (await async_session.scalars(software_query)).all()
        return len(remaining) == 1


def get_select_software_query(id_list: list[int]) -> Select[WikibaseSoftwareModel]:
    """Select WikibaseSoftwareModel in ID list"""

    software_query = select(WikibaseSoftwareModel).where(
        WikibaseSoftwareModel.id.in_(id_list)
    )

    return software_query


def get_update_software_tags_query(base_id: int, additional_id: int) -> Update:
    """Add Additional Software Tags to Base"""

    update_software_tags_query = software_tag_xref_table.insert().from_select(
        [
            software_tag_xref_table.c.wikibase_software_id,
            software_tag_xref_table.c.wikibase_software_tag_id,
        ],
        select(base_id, software_tag_xref_table.c.wikibase_software_tag_id).where(
            and_(
                software_tag_xref_table.c.wikibase_software_id == additional_id,
                software_tag_xref_table.c.wikibase_software_tag_id.not_in(
                    select(software_tag_xref_table.c.wikibase_software_tag_id).where(
                        software_tag_xref_table.c.wikibase_software_id == base_id
                    )
                ),
            )
        ),
    )

    return update_software_tags_query


def get_update_software_version_query(base_id: int, additional_id: int) -> Update:
    """Update Software Version from Additional ID to Base ID"""

    update_software_version_query = (
        update(WikibaseSoftwareVersionModel)
        .where(WikibaseSoftwareVersionModel.software_id == additional_id)
        .values(software_id=base_id)
    )

    return update_software_version_query
