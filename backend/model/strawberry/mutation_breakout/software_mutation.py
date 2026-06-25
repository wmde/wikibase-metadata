"""Software-Related Mutations"""

import strawberry
from strawberry import Info

from resolvers.authentication import authenticate
from resolvers.update.merge_software import merge_software_by_id
from resolvers.update.set_extension_wbs_bundled import set_extension_wbs_bundled


@strawberry.type
class SoftwareMutation:
    """Software-Related Mutations"""

    @strawberry.mutation(description="Merge Software")
    async def merge_software_by_id(
        self, info: Info, base_id: int, additional_id: int
    ) -> bool:
        """Merge Software"""

        authenticate(info)
        return await merge_software_by_id(base_id, additional_id)

    @strawberry.mutation(description="Set Extension Bundled with WBS")
    async def set_extension_wbs_bundled(
        self, info: Info, extension_id: int, bundled: bool = True
    ) -> bool:
        """Set Extension Bundled with WBS"""

        authenticate(info)
        return await set_extension_wbs_bundled(extension_id, bundled)
