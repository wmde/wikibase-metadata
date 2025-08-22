"""Wikibase URL Observation Table"""

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseURLObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase URL Observation Table"""

    __tablename__ = "wikibase_url_observation"

    total_url_properties: Mapped[Optional[int]] = mapped_column(
        "total_url_properties", Integer, nullable=True
    )
    """Total Url Properties"""

    total_url_statements: Mapped[Optional[int]] = mapped_column(
        "total_url_statements", Integer, nullable=True
    )
    """Total Statements using Url Properties"""

