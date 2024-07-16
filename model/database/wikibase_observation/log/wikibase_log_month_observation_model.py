"""Wikibase Log Observation Table"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.log.wikibase_log_month_type_observation_model import (
    WikibaseLogMonthTypeObservationModel,
)


class WikibaseLogMonthObservationModel(ModelBase):
    """Wikibase Log Month Observation Table"""

    __tablename__ = "wikibase_log_observation_month"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    first_log_date: Mapped[Optional[datetime]] = mapped_column(
        "first_log_date", DateTime(timezone=True), nullable=True
    )
    """Oldest Log Date"""

    last_log_date: Mapped[Optional[datetime]] = mapped_column(
        "last_log_date", DateTime(timezone=True), nullable=True
    )
    """Newest Log Date"""

    log_count: Mapped[int] = mapped_column("log_count", Integer, nullable=False)
    """Number of Logs"""

    user_count: Mapped[int] = mapped_column("user_count", Integer, nullable=False)
    """Number of Unique Users"""

    human_user_count: Mapped[int] = mapped_column(
        "user_count_no_bot", Integer, nullable=True
    )
    """Number of Unique Users, Without Bots"""

    log_type_records: Mapped[List[WikibaseLogMonthTypeObservationModel]] = relationship(
        "WikibaseLogMonthTypeObservationModel", lazy="selectin"
    )
    """Log Type Observations"""

    def __str__(self) -> str:
        return (
            "WikibaseLogMonthObservationModel("
            + f"id={self.id}, "
            + f"first_log_date={self.first_log_date}, "
            + f"last_log_date={self.last_log_date}, "
            + f"log_count={self.log_count}, "
            + f"user_count={self.user_count}, "
            + f"human_user_count={self.human_user_count}"
            + ")"
        )
