"""Wikibase Item Creation Date Table"""

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase


class WikibaseItemDateModel(ModelBase):
    """Wikibase Item Date Table"""

    __tablename__ = "wikibase_item_date"

    __table_args__ = (
        UniqueConstraint(
            "wikibase_time_to_first_value_observation_id", "q", name="unique_observation_q"
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_time_to_first_value_observation_id: Mapped[int] = mapped_column(
        "wikibase_time_to_first_value_observation_id",
        ForeignKey(
            column="wikibase_time_to_first_value_observation.id", name="observation"
        ),
        nullable=False,
    )
    """Wikibase Time to First Value Observation ID"""

    item_number: Mapped[int] = mapped_column("q", Integer, nullable=False)
    """Q#"""

    creation_date: Mapped[datetime] = mapped_column(
        "creation_date", DateTime(timezone=True), nullable=False
    )
