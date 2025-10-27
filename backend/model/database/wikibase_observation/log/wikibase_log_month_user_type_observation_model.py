"""Wikibase Log Month User Observation Table"""

from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.enum import WikibaseUserType


class WikibaseLogMonthUserTypeObservationModel(ModelBase):
    """Wikibase Log Month User Observation Table"""

    __tablename__ = "wikibase_log_observation_month_user"

    __table_args__ = (
        UniqueConstraint(
            "log_month_observation_id", "user_type", name="unique_observation_user_type"
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    log_month_observation_id: Mapped[int] = mapped_column(
        "log_month_observation_id",
        ForeignKey(
            column="wikibase_log_observation_month.id", name="month_observation"
        ),
        nullable=False,
    )
    """Log Month Observation ID"""

    user_type: Mapped[WikibaseUserType] = mapped_column(
        "user_type", Enum(WikibaseUserType), nullable=False
    )
    """Log Type"""

    first_log_date: Mapped[datetime] = mapped_column(
        "first_log_date", DateTime(timezone=True), nullable=False
    )
    """Oldest Log Date"""

    last_log_date: Mapped[datetime] = mapped_column(
        "last_log_date", DateTime(timezone=True), nullable=False
    )
    """Newest Log Date"""

    log_count: Mapped[int] = mapped_column("log_count", Integer, nullable=False)
    """Number of Logs"""

    user_count: Mapped[int] = mapped_column("user_count", Integer, nullable=False)
    """Number of Unique Users"""

    active_user_count: Mapped[Optional[int]] = mapped_column(
        "user_count_five_plus", Integer, nullable=True
    )
    """Number of Unique Users, 5+ Records"""

    def __str__(self) -> str:
        return (
            "WikibaseLogMonthUserObservationModel("
            + f"id={self.id}, "
            + f"user_type={self.user_type}, "
            + f"first_log_date={self.first_log_date}, "
            + f"last_log_date={self.last_log_date}, "
            + f"log_count={self.log_count}, "
            + f"user_count={self.user_count}"
            + ")"
        )
