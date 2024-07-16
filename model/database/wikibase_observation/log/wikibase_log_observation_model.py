"""Wikibase Log Observation Table"""

from datetime import datetime
import enum
from typing import Optional
from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import (
    WikibaseLogMonthObservationModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseUserType(enum.Enum):
    """Wikibase User Type"""

    BOT = 1
    MISSING = 2
    USER = 3
    NONE = 4


class WikibaseLogObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Log Observation Table"""

    __tablename__ = "wikibase_log_observation"

    first_log_date: Mapped[Optional[datetime]] = mapped_column(
        "first_log_date", DateTime(timezone=True), nullable=True
    )
    """Oldest Log Date"""

    last_log_date: Mapped[Optional[datetime]] = mapped_column(
        "last_log_date", DateTime(timezone=True), nullable=True
    )
    """Most Recent Log Date"""

    last_log_user_type: Mapped[Optional[WikibaseUserType]] = mapped_column(
        "last_log_user_type", Enum(WikibaseUserType), nullable=True
    )
    """Most Recent Log - User or Bot?"""

    first_month_id: Mapped[Optional[int]] = mapped_column(
        "first_month_id",
        ForeignKey(column="wikibase_log_observation_month.id", name="first_month"),
        nullable=True,
    )

    first_month: Mapped[Optional[WikibaseLogMonthObservationModel]] = relationship(
        "WikibaseLogMonthObservationModel",
        lazy="selectin",
        primaryjoin=first_month_id == WikibaseLogMonthObservationModel.id
    )

    last_month_id: Mapped[Optional[int]] = mapped_column(
        "last_month_id",
        ForeignKey(column="wikibase_log_observation_month.id", name="last_month"),
        nullable=True,
    )

    last_month: Mapped[Optional[WikibaseLogMonthObservationModel]] = relationship(
        "WikibaseLogMonthObservationModel",
        lazy="selectin",
        primaryjoin=last_month_id == WikibaseLogMonthObservationModel.id
    )

    last_month_log_count: Mapped[Optional[int]] = mapped_column(
        "last_month_log_count", Integer, nullable=True
    )
    """Number of Logs from 30 Days Since Observation"""

    last_month_user_count: Mapped[Optional[int]] = mapped_column(
        "last_month_user_count", Integer, nullable=True
    )
    """Unique Number of Users Logged in 30 Days Since Observation"""

    last_month_human_user_count: Mapped[Optional[int]] = mapped_column(
        "last_month_user_count_no_bot", Integer, nullable=True
    )
    """Unique Number of Users Logged in 30 Days Since Observation, Without Bots"""

    def __str__(self) -> str:
        return (
            "WikibaseLogObservationModel("
            + f"id={self.id}, "
            + f"observation_date={self.observation_date}, "
            + f"first_log_date={self.first_log_date}, "
            + f"last_log_date={self.last_log_date}, "
            + f"last_log_by={self.last_log_user_type}, "
            + f"last_month_log_count={self.last_month_log_count}, "
            + f"last_month_user_count={self.last_month_user_count}, "
            + f"last_month_human_user_count={self.last_month_human_user_count}"
            + ")"
        )
