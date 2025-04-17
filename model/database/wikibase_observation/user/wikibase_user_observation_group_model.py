"""Wikibase User Observation / Group Table"""

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibaseUserObservationGroupModel(ModelBase):
    """Wikibase User Observation / Group Table"""

    __tablename__ = "wikibase_user_observation_group"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_user_observation_id: Mapped[int] = mapped_column(
        "wikibase_user_observation_id",
        ForeignKey(column="wikibase_user_observation.id", name="observation"),
        nullable=False,
    )
    """Wikibase User Observation ID"""

    user_observation: Mapped["WikibaseUserObservationModel"] = relationship(  # type: ignore
        "WikibaseUserObservationModel",
        back_populates="user_group_observations",
        lazy="selectin",
    )
    """User Observation"""

    wikibase_user_group_id: Mapped[int] = mapped_column(
        "wikibase_user_group_id",
        ForeignKey(column="wikibase_user_group.id", name="group"),
        nullable=False,
    )
    """Wikibase User Group ID"""

    user_group: Mapped["WikibaseUserGroupModel"] = relationship(  # type: ignore
        "WikibaseUserGroupModel",
        back_populates="user_group_observations",
        lazy="selectin",
    )
    """User Group"""

    user_count: Mapped[int] = mapped_column("user_count", Integer, nullable=False)
    """User Count"""

    group_implicit: Mapped[bool] = mapped_column(
        "implicit", Boolean, nullable=False, default=False
    )
    """Group Implicit?"""
