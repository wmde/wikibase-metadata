"""Wikibase Log Observation Table"""

from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import (
    WikibaseLogMonthObservationModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)
from model.enum import WikibaseUserType


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
    """Most Recent Log User Type - User or Bot?"""

    first_month_id: Mapped[Optional[int]] = mapped_column(
        "first_month_id",
        ForeignKey(column="wikibase_log_observation_month.id", name="first_month"),
        nullable=True,
    )
    """First Month ID"""

    first_month: Mapped[Optional[WikibaseLogMonthObservationModel]] = relationship(
        "WikibaseLogMonthObservationModel",
        lazy="selectin",
        primaryjoin=first_month_id == WikibaseLogMonthObservationModel.id,
    )
    """First Month Log Record"""

    last_month_id: Mapped[Optional[int]] = mapped_column(
        "last_month_id",
        ForeignKey(column="wikibase_log_observation_month.id", name="last_month"),
        nullable=True,
    )
    """Last Month ID"""

    last_month: Mapped[Optional[WikibaseLogMonthObservationModel]] = relationship(
        "WikibaseLogMonthObservationModel",
        lazy="selectin",
        primaryjoin=last_month_id == WikibaseLogMonthObservationModel.id,
    )
    """Last Month Log Record"""

    def __str__(self) -> str:
        return (
            "WikibaseLogObservationModel("
            + f"id={self.id}, "
            + f"observation_date={self.observation_date}, "
            + f"first_log_date={self.first_log_date}, "
            + f"last_log_date={self.last_log_date}, "
            + f"last_log_by={self.last_log_user_type}"
            + ")"
        )
