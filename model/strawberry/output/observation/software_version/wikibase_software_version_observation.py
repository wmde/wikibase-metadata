"""Wikibase Software Version Observation Strawberry Model"""

from typing import List
import strawberry

from model.database import (
    WikibaseSoftwareVersionObservationModel,
)
from model.database.wikibase_observation.version.software_version_model import (
    WikibaseSoftwareTypes,
)
from model.strawberry.output.observation.software_version.wikibase_software_version import (
    WikibaseSoftwareVersionStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)


@strawberry.type
class WikibaseSoftwareVersionObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Software Version Observation"""

    installed_extensions: List[
        WikibaseSoftwareVersionStrawberryModel
    ] = strawberry.field(description="Installed Extensions w/ Versions")

    installed_libraries: List[
        WikibaseSoftwareVersionStrawberryModel
    ] = strawberry.field(description="Installed Libraries w/ Versions")

    installed_skins: List[WikibaseSoftwareVersionStrawberryModel] = strawberry.field(
        description="Installed Skins w/ Versions"
    )

    installed_software: List[WikibaseSoftwareVersionStrawberryModel] = strawberry.field(
        description="Installed Software Versions"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseSoftwareVersionObservationModel
    ) -> "WikibaseSoftwareVersionObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            installed_extensions=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software_type == WikibaseSoftwareTypes.extension
                ],
                key=lambda x: x.software_name,
            ),
            installed_libraries=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software_type == WikibaseSoftwareTypes.library
                ],
                key=lambda x: x.software_name,
            ),
            installed_skins=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software_type == WikibaseSoftwareTypes.skin
                ],
                key=lambda x: x.software_name,
            ),
            installed_software=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software_type == WikibaseSoftwareTypes.software
                ],
                key=lambda x: x.software_name,
            ),
        )
