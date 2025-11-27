"""Wikibase Quantity Observation Table"""

from typing import Optional
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseQuantityObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Quantity Observation Table"""

    __tablename__ = "wikibase_quantity_observation"

    total_items: Mapped[Optional[int]] = mapped_column(
        "total_items", BigInteger, nullable=True
    )
    """Total Items"""

    total_lexemes: Mapped[Optional[int]] = mapped_column(
        "total_lexemes", BigInteger, nullable=True
    )
    """Total Lexemes"""

    total_properties: Mapped[Optional[int]] = mapped_column(
        "total_properties", BigInteger, nullable=True
    )
    """Total Properties"""

    total_triples: Mapped[Optional[int]] = mapped_column(
        "total_triples", BigInteger, nullable=True
    )
    """Total Triples"""
