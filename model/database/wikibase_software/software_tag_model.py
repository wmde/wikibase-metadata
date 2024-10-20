"""Wikibase Software Version Table"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase


class WikibaseSoftwareTagModel(ModelBase):
    """Wikibase Software Tag Table"""

    __tablename__ = "wikibase_software_tag"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    tag: Mapped[str] = mapped_column("tag", String, nullable=False, unique=True)
    """Software Tag"""

    def __init__(self, tag: str):
        self.tag = tag

    def __str__(self) -> str:
        return f"WikibaseSoftwareTagModel(id={self.id}, tag={self.tag})"
