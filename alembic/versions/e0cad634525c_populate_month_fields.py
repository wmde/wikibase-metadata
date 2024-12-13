"""Populate Month Fields

Revision ID: e0cad634525c
Revises: d6c7d96ba079
Create Date: 2024-11-18 13:21:35.815575

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from model.database.wikibase_observation.log.wikibase_log_month_observation_model import (
    WikibaseLogMonthObservationModel,
)
from model.enum import WikibaseUserType


# revision identifiers, used by Alembic.
revision: str = "e0cad634525c"
down_revision: Union[str, None] = "d6c7d96ba079"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


WikibaseLogObservationModel = (
    sa.text(
        """
SELECT
    id,
    wikibase_id,
    anything AS returned_data,
    date AS observation_date,
    first_log_date,
    last_log_date,
    last_log_user_type,
    first_month_id,
    last_month_id
FROM wikibase_log_observation"""
    )
    .columns(
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("wikibase_id", sa.Integer, nullable=False),
        sa.Column("returned_data", sa.Boolean, nullable=False),
        sa.Column("observation_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_log_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_log_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_log_user_type", sa.Enum(WikibaseUserType), nullable=True),
        sa.Column("first_month_id", sa.Integer, nullable=True),
        sa.Column("last_month_id", sa.Integer, nullable=True),
    )
    .cte()
)


def upgrade() -> None:
    # Update existing records
    wikibase_id_scalar_subq = (
        sa.select(WikibaseLogObservationModel.c.wikibase_id)
        .where(
            sa.or_(
                WikibaseLogObservationModel.c.first_month_id
                == WikibaseLogMonthObservationModel.id,
                WikibaseLogObservationModel.c.last_month_id
                == WikibaseLogMonthObservationModel.id,
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    returned_data_scalar_subq = (
        sa.select(WikibaseLogObservationModel.c.returned_data)
        .where(
            sa.or_(
                WikibaseLogObservationModel.c.first_month_id
                == WikibaseLogMonthObservationModel.id,
                WikibaseLogObservationModel.c.last_month_id
                == WikibaseLogMonthObservationModel.id,
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    observation_date_scalar_subq = (
        sa.select(WikibaseLogObservationModel.c.observation_date)
        .where(
            sa.or_(
                WikibaseLogObservationModel.c.first_month_id
                == WikibaseLogMonthObservationModel.id,
                WikibaseLogObservationModel.c.last_month_id
                == WikibaseLogMonthObservationModel.id,
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    first_month_scalar_subq = (
        sa.select(
            (
                sa.and_(
                    WikibaseLogObservationModel.c.first_month_id != None,
                    WikibaseLogObservationModel.c.first_month_id
                    == WikibaseLogMonthObservationModel.id,
                )
            ).label("first_month")
        )
        .where(
            sa.or_(
                WikibaseLogObservationModel.c.first_month_id
                == WikibaseLogMonthObservationModel.id,
                WikibaseLogObservationModel.c.last_month_id
                == WikibaseLogMonthObservationModel.id,
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    last_log_user_type_scalar_subq = (
        sa.select(
            sa.case(
                (
                    sa.and_(
                        WikibaseLogObservationModel.c.last_month_id != None,
                        WikibaseLogObservationModel.c.last_month_id
                        == WikibaseLogMonthObservationModel.id,
                    ),
                    WikibaseLogObservationModel.c.last_log_user_type,
                ),
                else_=None,
            ).label("last_log_user_type")
        )
        .where(
            sa.or_(
                WikibaseLogObservationModel.c.first_month_id
                == WikibaseLogMonthObservationModel.id,
                WikibaseLogObservationModel.c.last_month_id
                == WikibaseLogMonthObservationModel.id,
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    update_query = sa.update(WikibaseLogMonthObservationModel).values(
        wikibase_id=wikibase_id_scalar_subq,
        returned_data=returned_data_scalar_subq,
        observation_date=observation_date_scalar_subq,
        first_month=first_month_scalar_subq,
        last_log_user_type=last_log_user_type_scalar_subq,
    )

    op.execute(update_query)

    # Populate empty records
    op.execute(
        sa.insert(WikibaseLogMonthObservationModel).from_select(
            [
                WikibaseLogMonthObservationModel.wikibase_id,
                WikibaseLogMonthObservationModel.returned_data,
                WikibaseLogMonthObservationModel.observation_date,
                WikibaseLogMonthObservationModel.first_month,
            ],
            sa.union_all(
                sa.select(
                    WikibaseLogObservationModel.c.wikibase_id,
                    WikibaseLogObservationModel.c.returned_data,
                    WikibaseLogObservationModel.c.observation_date,
                    False,
                ).where(sa.not_(WikibaseLogObservationModel.c.returned_data)),
                sa.select(
                    WikibaseLogObservationModel.c.wikibase_id,
                    WikibaseLogObservationModel.c.returned_data,
                    WikibaseLogObservationModel.c.observation_date,
                    True,
                ).where(sa.not_(WikibaseLogObservationModel.c.returned_data)),
            ),
        )
    )


def downgrade() -> None:
    partition_subq = (
        sa.select(
            WikibaseLogMonthObservationModel,
            sa.func.rank()
            .over(
                partition_by=[
                    WikibaseLogMonthObservationModel.wikibase_id,
                    WikibaseLogMonthObservationModel.returned_data,
                    WikibaseLogMonthObservationModel.observation_date,
                ],
                order_by=sa.not_(WikibaseLogMonthObservationModel.first_month),
            )
            .label("month_rank"),
        )
        .subquery()
        .alias("partition_subq")
    )
    max_rank_subq = (
        sa.select(
            partition_subq.c.wikibase_id,
            partition_subq.c.anything,
            partition_subq.c.date,
            sa.func.max(partition_subq.c.month_rank).label("max_rank"),
        )
        .group_by(
            partition_subq.c.wikibase_id,
            partition_subq.c.anything,
            partition_subq.c.date,
        )
        .subquery()
        .alias("max_rank_subq")
    )

    # Will always be the last month of an observation
    last_month_subq = (
        sa.select(partition_subq)
        .join(
            max_rank_subq,
            onclause=sa.and_(
                partition_subq.c.wikibase_id == max_rank_subq.c.wikibase_id,
                partition_subq.c.anything == max_rank_subq.c.anything,
                partition_subq.c.date == max_rank_subq.c.date,
                partition_subq.c.month_rank == max_rank_subq.c.max_rank,
            ),
        )
        .subquery()
        .alias("max_partition_subq")
    )
    # Will always be the first month of an observation
    first_month_subq = (
        (sa.select(partition_subq).where(partition_subq.c.month_rank == 1))
        .subquery()
        .alias("min_partition_subq")
    )

    op.execute(
        sa.insert(WikibaseLogObservationModel).from_select(
            [
                WikibaseLogObservationModel.c.wikibase_id,
                WikibaseLogObservationModel.c.returned_data,
                WikibaseLogObservationModel.c.observation_date,
                WikibaseLogObservationModel.c.first_log_date,
                WikibaseLogObservationModel.c.last_log_date,
                WikibaseLogObservationModel.c.last_log_user_type,
                WikibaseLogObservationModel.c.first_month_id,
                WikibaseLogObservationModel.c.last_month_id,
            ],
            sa.select(
                first_month_subq.c.wikibase_id,
                first_month_subq.c.anything,
                first_month_subq.c.date,
                first_month_subq.c.first_log_date,
                last_month_subq.c.last_log_date,
                last_month_subq.c.last_log_user_type,
                first_month_subq.c.id.label("first_month_id"),
                last_month_subq.c.id.label("last_month_id"),
            ).join_from(
                first_month_subq,
                last_month_subq,
                onclause=sa.and_(
                    first_month_subq.c.wikibase_id == last_month_subq.c.wikibase_id,
                    first_month_subq.c.anything == last_month_subq.c.anything,
                    first_month_subq.c.date == last_month_subq.c.date,
                ),
            ),
        )
    )
