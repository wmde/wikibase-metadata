"""Wikibase Log Month Observation Table"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.log.wikibase_log_month_log_type_observation_model import (
    WikibaseLogMonthLogTypeObservationModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_user_type_observation_model import (
    WikibaseLogMonthUserTypeObservationModel,
)
from model.enum import WikibaseUserType


class WikibaseLogMonthObservationModel(ModelBase):
    """Wikibase Log Month Observation Table"""

    __tablename__ = "wikibase_log_observation_month"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_id: Mapped[Optional[int]] = mapped_column(
        "wikibase_id",
        ForeignKey(column="wikibase.id", name="observation_wikibase"),
        nullable=True,
    )
    """Wikibase ID"""

    returned_data: Mapped[Optional[bool]] = mapped_column(
        "anything", Boolean, nullable=True
    )
    """Returned Data?"""

    observation_date: Mapped[Optional[datetime]] = mapped_column(
        "date",
        DateTime(timezone=True),
        nullable=True,
        # pylint: disable=not-callable
        default=func.now(),
    )
    """Date"""

    first_month: Mapped[Optional[bool]] = mapped_column("first", Boolean, nullable=True)

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
