"""Wikibase Software Version Observation Strawberry Model"""

import strawberry

from model.database import WikibaseSoftwareVersionObservationModel
from model.enum import WikibaseSoftwareType
from model.strawberry.output.observation.software_version.software_version import (
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

    installed_extensions: list[WikibaseSoftwareVersionStrawberryModel] = (
        strawberry.field(description="Installed Extensions w/ Versions")
    )

    installed_libraries: list[WikibaseSoftwareVersionStrawberryModel] = (
        strawberry.field(description="Installed Libraries w/ Versions")
    )

    installed_skins: list[WikibaseSoftwareVersionStrawberryModel] = strawberry.field(
        description="Installed Skins w/ Versions"
    )

    installed_software: list[WikibaseSoftwareVersionStrawberryModel] = strawberry.field(
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
                    if o.software.software_type == WikibaseSoftwareType.EXTENSION
                ],
                key=lambda x: x.software_name,
            ),
            installed_libraries=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software.software_type == WikibaseSoftwareType.LIBRARY
                ],
                key=lambda x: x.software_name,
            ),
            installed_skins=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software.software_type == WikibaseSoftwareType.SKIN
                ],
                key=lambda x: x.software_name,
            ),
            installed_software=sorted(
                [
                    WikibaseSoftwareVersionStrawberryModel.marshal(o)
                    for o in model.software_versions
                    if o.software.software_type == WikibaseSoftwareType.SOFTWARE
                ],
                key=lambda x: x.software_name,
            ),
        )
