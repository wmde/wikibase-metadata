"""Wikibase Recent Changes Observation Table"""

from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseRecentChangesObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Recent Changes Observation Table"""

    __tablename__ = "wikibase_recent_changes_observation"

    human_change_count: Mapped[int] = mapped_column(Integer, nullable=True)
    """Number of changes (excluding bots)"""

    human_change_user_count: Mapped[int] = mapped_column(Integer, nullable=True)
    """Number of unique users (excluding bots)"""

    human_change_active_user_count: Mapped[int] = mapped_column(
        "human_change_user_count_five_plus", Integer, nullable=True
    )
    """Number of unique users (excluding bots) with at least 5 changes"""

    bot_change_count: Mapped[int] = mapped_column(Integer, nullable=True)
    """Total number of changes (including bots)"""

    bot_change_user_count: Mapped[int] = mapped_column(Integer, nullable=True)
    """Total number of unique users (including bots)"""

    bot_change_active_user_count: Mapped[int] = mapped_column(
        "bot_change_user_count_five_plus", Integer, nullable=True
    )
    """Total number of unique users (including bots) with at least 5 changes"""

    first_change_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    """Date of first change"""

    last_change_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    """Date of last change"""
