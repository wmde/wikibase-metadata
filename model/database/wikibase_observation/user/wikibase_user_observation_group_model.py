"""Wikibase User Observation / Group"""

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibaseUserObservationGroupModel(ModelBase):
    """Wikibase User Observation / Group"""

    __tablename__ = "wikibase_user_observation_group"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_user_observation_id = mapped_column(
        "wikibase_user_observation_id",
        ForeignKey("wikibase_user_observation.id", None, False, "observation"),
        nullable=False,
    )
    """Wikibase User Observation ID"""

    user_observation: Mapped["WikibaseUserObservationModel"] = relationship(
        "WikibaseUserObservationModel",
        back_populates="user_group_observations",
        lazy="selectin",
    )
    """User Observation"""

    wikibase_user_group_id = mapped_column(
        "wikibase_user_group_id",
        ForeignKey("wikibase_user_group.id", None, False, "group"),
        nullable=False,
    )
    """Wikibase User Group ID"""

    user_group: Mapped["WikibaseUserGroupModel"] = relationship(
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
