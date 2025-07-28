"""Wikibase Recent Changes Observation Table"""

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseRecentChangesObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Recent Changes Observation Table"""

    __tablename__ = "wikibase_recent_changes_observation"

    change_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    """Number of changes"""

    user_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    """Number of unique users"""

    first_change_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    """Date of first change"""

    last_change_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    """Date of last change"""

    # wikibase_id = Column(
    #     Integer,
    #     ForeignKey("wikibase.id", name="foreign_key_wikibase_id"),
    #     nullable=False,
    #     index=True,
    # )
    #
    # __mapper_args__ = {"polymorphic_identity": "recent_changes"}
