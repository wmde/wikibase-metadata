"""Wikibase Software Version Table"""

from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_software import WikibaseSoftwareModel


class WikibaseSoftwareVersionModel(ModelBase):
    """Wikibase Software Version Table"""

    __tablename__ = "wikibase_software_version"

    __table_args__ = (
        UniqueConstraint(
            "wikibase_software_version_observation_id",
            "wikibase_software_id",
            name="unique_observation_software_id",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_software_version_observation_id: Mapped[int] = mapped_column(
        "wikibase_software_version_observation_id",
        ForeignKey(
            column="wikibase_software_version_observation.id", name="observation"
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

    software_id: Mapped[int] = mapped_column(
        "wikibase_software_id",
        ForeignKey(column="wikibase_software.id", name="software"),
        nullable=False,
    )
    """Software Id"""

    software: Mapped[WikibaseSoftwareModel] = relationship(
        "WikibaseSoftwareModel",
        # back_populates="software_versions",
        lazy="selectin",
    )
    """Software"""

    version: Mapped[Optional[str]] = mapped_column("version", String, nullable=True)
    """Version"""

    version_hash: Mapped[Optional[str]] = mapped_column(
        "version_hash", String, nullable=True
    )
    """Version Hash"""

    version_date: Mapped[Optional[datetime]] = mapped_column(
        "version_date", DateTime, nullable=True
    )
    """Version Date"""

    def __init__(
        self,
        software: WikibaseSoftwareModel,
        version: str,
        version_hash: Optional[str] = None,
        version_date: Optional[datetime] = None,
    ):
        self.software = software

        self.version_hash = (
            None
            if version_hash is None
            else version_hash.replace("(", "").replace(")", "")
        )
        self.version_date = version_date
        self.version = version if version != "–" else self.version_hash

    def __str__(self) -> str:
        return (
            "WikibaseSoftwareVersionModel("
            + f"software_type={self.software.software_type}, "
            + f"software_name={self.software.software_name}, "
            + f"version={self.version}, "
            + f"version_date={self.version_date}, "
            + f"version_hash={self.version_hash})"
        )
