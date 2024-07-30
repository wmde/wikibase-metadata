"""Wikibase Log Observation Table"""

from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.enum import WikibaseLogType


class WikibaseLogMonthLogTypeObservationModel(ModelBase):
    """Wikibase Log Month Type Observation Table"""

    __tablename__ = "wikibase_log_observation_month_type"

    __table_args__ = (
        UniqueConstraint(
            "log_month_observation_id",
            "log_type",
            name="unique_observation_log_type",
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

    log_type: Mapped[WikibaseLogType] = mapped_column(
        "log_type", Enum(WikibaseLogType), nullable=False
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

    human_user_count: Mapped[int] = mapped_column(
        "user_count_no_bot", Integer, nullable=True
    )
    """Number of Unique Users, Without Bots"""

    def __str__(self) -> str:
        return (
            "WikibaseLogMonthTypeObservationModel("
            + f"id={self.id}, "
            + f"log_type={self.log_type}, "
            + f"first_log_date={self.first_log_date}, "
            + f"last_log_date={self.last_log_date}, "
            + f"log_count={self.log_count}, "
            + f"user_count={self.user_count}, "
            + f"human_user_count={self.human_user_count}"
            + ")"
        )
