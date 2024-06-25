"""Wikibase Software Version Table"""

from datetime import datetime
import enum
from typing import Optional
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibaseSoftwareTypes(enum.Enum):
    software = 1
    skin = 2
    extension = 3
    library = 4


class WikibaseSoftwareVersionModel(ModelBase):
    """Wikibase Software Version Table"""

    __tablename__ = "wikibase_software_version"

    __table_args__ = (
        UniqueConstraint(
            "wikibase_software_version_observation_id",
            "software_type",
            "software_name",
            name="unique_observation_software_type_name",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_software_version_observation_id: Mapped[int] = mapped_column(
        "wikibase_software_version_observation_id",
        ForeignKey(
            "wikibase_software_version_observation.id", None, False, "observation"
        ),
        nullable=False,
    )
    """Wikibase Software Version Observation ID"""

    wikibase_software_version_observation: Mapped[
        "WikibaseSoftwareVersionObservationModel"
    ] = relationship(
        "WikibaseSoftwareVersionObservationModel",
        back_populates="software_versions",
        lazy="selectin",
    )
    """Software Version Observation"""

    software_type = mapped_column(
        "software_type", Enum(WikibaseSoftwareTypes), nullable=False
    )
    """Software Type"""

    software_name: Mapped[str] = mapped_column("software_name", String, nullable=False)
    """Software Name"""

    version: Mapped[str] = mapped_column("version", String, nullable=False)
    """Version"""

    version_hash: Mapped[Optional[str]] = mapped_column(
        "version_hash", String, nullable=True
    )
    """Version Hash"""

    version_date: Mapped[Optional[datetime]] = mapped_column(
        "version_date", DateTime, nullable=True
    )
    """Version Date"""
