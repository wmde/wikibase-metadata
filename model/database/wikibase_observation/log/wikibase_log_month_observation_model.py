"""Wikibase Log Month Observation Table"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Boolean, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.log.wikibase_log_month_log_type_observation_model import (
    WikibaseLogMonthLogTypeObservationModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_user_type_observation_model import (
    WikibaseLogMonthUserTypeObservationModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)
from model.enum import WikibaseUserType


class WikibaseLogMonthObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Log Month Observation Table"""

    __tablename__ = "wikibase_log_observation_month"

    first_month: Mapped[bool] = mapped_column("first", Boolean, nullable=False)

    first_log_date: Mapped[Optional[datetime]] = mapped_column(
        "first_log_date", DateTime(timezone=True), nullable=True
    )
    """Oldest Log Date"""

    last_log_date: Mapped[Optional[datetime]] = mapped_column(
        "last_log_date", DateTime(timezone=True), nullable=True
    )
    """Newest Log Date"""

    last_log_user_type: Mapped[Optional[WikibaseUserType]] = mapped_column(
        "last_log_user_type", Enum(WikibaseUserType), nullable=True
    )
    """Most Recent Log User Type - User or Bot?"""

    log_count: Mapped[Optional[int]] = mapped_column(
        "log_count", Integer, nullable=True
    )
    """Number of Logs"""

    user_count: Mapped[Optional[int]] = mapped_column(
        "user_count", Integer, nullable=True
    )
    """Number of Unique Users"""

    human_user_count: Mapped[Optional[int]] = mapped_column(
        "user_count_no_bot", Integer, nullable=True
    )
    """Number of Unique Users, Without Bots"""

    log_type_records: Mapped[list[WikibaseLogMonthLogTypeObservationModel]] = (
        relationship("WikibaseLogMonthLogTypeObservationModel", lazy="selectin")
    )
    """Log Type Observations"""

    user_type_records: Mapped[list[WikibaseLogMonthUserTypeObservationModel]] = (
        relationship("WikibaseLogMonthUserTypeObservationModel", lazy="selectin")
    )
    """User Type Observations"""

    def __init__(self, wikibase_id: int, first_month: bool):
        self.wikibase_id = wikibase_id
        self.first_month = first_month
        self.observation_date = datetime.now(tz=timezone.utc)

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
