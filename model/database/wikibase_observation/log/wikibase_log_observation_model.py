"""Wikibase Log Observation Table"""

from datetime import datetime
import enum
from sqlalchemy import DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseUserType(enum.Enum):
    """Wikibase User Type"""

    BOT = 1
    USER = 2


class WikibaseLogObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Log Observation Table"""

    __tablename__ = "wikibase_log_observation"

    first_log_date: Mapped[datetime] = mapped_column(
        "first_log_date", DateTime(timezone=True), nullable=False
    )
    """Oldest Log Date"""

    last_log_date: Mapped[datetime] = mapped_column(
        "last_log_date", DateTime(timezone=True), nullable=False
    )
    """Most Recent Log Date"""

    last_log_user_type: Mapped[WikibaseUserType] = mapped_column(
        "last_log_user_type", Enum(WikibaseUserType), nullable=False
    )
    """Most Recent Log - User or Bot?"""

    last_month_log_count: Mapped[int] = mapped_column(
        "last_month_log_count", Integer, nullable=False
    )
    """Number of Logs from 30 Days Since Observation"""

    last_month_user_count: Mapped[int] = mapped_column(
        "last_month_user_count", Integer, nullable=False
    )
    """Unique Number of Users Logged in 30 Days Since Observation"""

    last_month_human_user_count: Mapped[int] = mapped_column(
        "last_month_user_count_no_bot", Integer, nullable=False
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