"""Wikibase Statistics Observation Table"""

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseStatisticsObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Statistics Observation Table"""

    __tablename__ = "wikibase_statistics_observation"

    total_pages: Mapped[Optional[int]] = mapped_column(
        "total_pages", Integer, nullable=True
    )
    """Total Pages"""

    content_pages: Mapped[Optional[int]] = mapped_column(
        "content_pages", Integer, nullable=True
    )
    """Total Content Pages"""

    total_files: Mapped[Optional[int]] = mapped_column(
        "total_files", Integer, nullable=True
    )
    """Total Files"""

    total_edits: Mapped[Optional[int]] = mapped_column(
        "total_edits", Integer, nullable=True
    )
    """Total Edits"""

    content_page_word_count_total: Mapped[Optional[int]] = mapped_column(
        "content_words", Integer, nullable=True
    )
    """Words in Content Pages"""

    total_users: Mapped[Optional[int]] = mapped_column(
        "total_users", Integer, nullable=True
    )
    """Total Users"""

    active_users: Mapped[Optional[int]] = mapped_column(
        "active_users", Integer, nullable=True
    )
    """Users Active in 30 Days"""

    total_admin: Mapped[Optional[int]] = mapped_column(
        "total_admin", Integer, nullable=True
    )
    """Total Admin"""
