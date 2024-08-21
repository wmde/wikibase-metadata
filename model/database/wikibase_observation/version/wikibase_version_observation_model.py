"""Wikibase Software Version Observation Table"""

from typing import List
from sqlalchemy.orm import Mapped, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.version.software_version_model import (
    WikibaseSoftwareVersionModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseSoftwareVersionObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Software Version Observation Table"""

    __tablename__ = "wikibase_software_version_observation"

    software_versions: Mapped[List[WikibaseSoftwareVersionModel]] = relationship(
        "WikibaseSoftwareVersionModel",
        back_populates="wikibase_software_version_observation",
        lazy="selectin",
    )
    """Software Versions"""
