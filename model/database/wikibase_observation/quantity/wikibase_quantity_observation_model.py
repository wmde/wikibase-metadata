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
    """Total Items"""

    total_lexemes: Mapped[Optional[int]] = mapped_column(
        "total_lexemes", Integer, nullable=True
    )
    """Total Lexemes"""

    total_properties: Mapped[Optional[int]] = mapped_column(
        "total_properties", Integer, nullable=True
    )
    """Total Properties"""

    total_triples: Mapped[Optional[int]] = mapped_column(
        "total_triples", Integer, nullable=True
    )
    """Total Triples"""

    total_external_identifier_properties: Mapped[Optional[int]] = mapped_column(
        "total_external_identifier_properties", Integer, nullable=True
    )
    """Total External Identifier Properties"""

    total_external_identifier_statements: Mapped[Optional[int]] = mapped_column(
        "total_external_identifier_statements", Integer, nullable=True
    )
    """Total Statements using External Identifier Properties"""

    total_url_properties: Mapped[Optional[int]] = mapped_column(
        "total_url_properties", Integer, nullable=True
    )
    """Total Url Properties"""

    total_url_statements: Mapped[Optional[int]] = mapped_column(
        "total_url_statements", Integer, nullable=True
    )
    """Total Statements using Url Properties"""
