"""Wikibase Log Observation Table"""

from datetime import datetime
import enum
from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase


class WikibaseLogType(enum.Enum):
    """Wikibase Log Type"""

    COMMENTS_CREATE = 1
    COMMENTS_DELETE = 2
    CONSUMER_APPROVE = 3
    CONSUMER_PROPOSE = 4
    IMAGE_UPLOAD = 5
    IMAGE_OVERWRITE = 6
    IMPORT = 7
    INTERWIKI_CREATE = 8
    INTERWIKI_DELETE = 9
    INTERWIKI_EDIT = 10
    ITEM_CREATE = 11
    ITEM_DELETE = 12
    MOVE = 13
    PAGE_CREATE = 14
    PAGE_DELETE = 15
    PATROL = 16
    PATROL_AUTO = 17
    PROPERTY_CREATE = 18
    PROPERTY_DELETE = 19
    PROTECT = 20
    UNDO_DELETE = 21
    USER_BLOCK = 22
    USER_UNBLOCK = 23
    USER_CREATE = 24
    USER_RIGHTS = 25


class WikibaseLogMonthTypeObservationModel(ModelBase):
    """Wikibase Log Month Type Observation Table"""

    __tablename__ = "wikibase_log_observation_month_type"

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
