"""Wikibase Quantity Observation Table"""

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseQuantityObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Quantity Observation Table"""

    __tablename__ = "wikibase_quantity_observation"

    total_items: Mapped[Optional[int]] = mapped_column(
        "total_items", Integer, nullable=True
    )
    total_lexemes: Mapped[Optional[int]] = mapped_column(
        "total_lexemes", Integer, nullable=True
    )
    total_properties: Mapped[Optional[int]] = mapped_column(
        "total_properties", Integer, nullable=True
    )
    total_triples: Mapped[Optional[int]] = mapped_column(
        "total_triples", Integer, nullable=True
    )
