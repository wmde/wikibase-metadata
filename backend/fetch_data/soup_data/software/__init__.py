"""Software Observations & Data"""

from fetch_data.soup_data.software.create_software_version_data_observation import (
    create_software_version_observation,
)
from fetch_data.soup_data.software.get_software_model import (
    get_or_create_software_model,
)
from fetch_data.soup_data.software.get_update_software_data import (
    fetch_or_create_tags,
    get_update_extension_query,
    update_software_data,
)
