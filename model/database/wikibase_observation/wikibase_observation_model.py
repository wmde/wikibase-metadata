"""Wikibase Observation Table - ABSTRACT"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


class WikibaseObservationModel:
    """Wikibase Observation Table - ABSTRACT"""

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_id: Mapped[int] = mapped_column(
        "wikibase_id",
        ForeignKey(column="wikibase.id", name="observation_wikibase"),
        nullable=False,
    )
    """Wikibase ID"""

    @declared_attr
    def wikibase(self) -> Mapped["WikibaseModel"]:
        """Wikibase"""
        return relationship("WikibaseModel", lazy="selectin")

    returned_data: Mapped[bool] = mapped_column("anything", Boolean, nullable=False)
    """Returned Data?"""

    observation_date: Mapped[datetime] = mapped_column(
        "date",
        DateTime(timezone=True),
        nullable=False,
        # pylint: disable-next=not-callable
        default=func.now(),
    )
    """Date"""
