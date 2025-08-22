"""Wikibase External Identifier Observation Table"""

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseExternalIdentifierObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase External Identifier Observation Table"""

    __tablename__ = "wikibase_external_identifier_observation"

    total_external_identifier_properties: Mapped[Optional[int]] = mapped_column(
        "total_external_identifier_properties", Integer, nullable=True
    )
    """Total External Identifier Properties"""

    total_external_identifier_statements: Mapped[Optional[int]] = mapped_column(
        "total_external_identifier_statements", Integer, nullable=True
    )
    """Total Statements using External Identifier Properties"""

