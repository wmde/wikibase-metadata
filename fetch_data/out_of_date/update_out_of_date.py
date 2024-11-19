"""Update Out of Date Observations"""

from fetch_data.api_data import create_log_observation, create_user_observation
from fetch_data.out_of_date.get_out_of_date_wikibases import (
    get_wikibase_list_with_out_of_date_connectivity_observations,
    get_wikibase_list_with_out_of_date_log_first_observations,
    get_wikibase_list_with_out_of_date_log_last_observations,
    get_wikibase_list_with_out_of_date_property_popularity_observations,
    get_wikibase_list_with_out_of_date_quantity_observations,
    get_wikibase_list_with_out_of_date_software_observations,
    get_wikibase_list_with_out_of_date_stats_observations,
    get_wikibase_list_with_out_of_date_user_observations,
)
from fetch_data.soup_data import (
    create_software_version_observation,
    create_special_statistics_observation,
    update_software_data,
)
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)


async def update_out_of_date_connectivity_observations():
    """Update Out of Date Connectivity Observations"""

    ood_con_obs = await get_wikibase_list_with_out_of_date_connectivity_observations()
    for wikibase in ood_con_obs:
        await create_connectivity_observation(wikibase.id)


async def update_out_of_date_log_first_observations():
    """Update Out of Date Log (First Month) Observations"""

    ood_log_obs = await get_wikibase_list_with_out_of_date_log_first_observations()
    for wikibase in ood_log_obs:
        await create_log_observation(wikibase.id, first_month=True)


async def update_out_of_date_log_last_observations():
    """Update Out of Date Log (Last Month) Observations"""

    ood_log_obs = await get_wikibase_list_with_out_of_date_log_last_observations()
    for wikibase in ood_log_obs:
        await create_log_observation(wikibase.id, first_month=False)


async def update_out_of_date_property_observations():
    """Update Out of Date Property Popularity Observations"""

    ood_prop_obs = (
        await get_wikibase_list_with_out_of_date_property_popularity_observations()
    )
    for wikibase in ood_prop_obs:
        await create_property_popularity_observation(wikibase.id)


async def update_out_of_date_quantity_observations():
    """Update Out of Date Quantity Observations"""

    ood_quant_obs = await get_wikibase_list_with_out_of_date_quantity_observations()
    for wikibase in ood_quant_obs:
        await create_quantity_observation(wikibase.id)


async def update_out_of_date_software_observations():
    """Update Out of Date Software Version Observations"""

    ood_soft_obs = await get_wikibase_list_with_out_of_date_software_observations()
    for wikibase in ood_soft_obs:
        await create_software_version_observation(wikibase.id)
    await update_software_data()


async def update_out_of_date_stats_observations():
    """Update Out of Date Special:Statistics Observations"""

    ood_stats_obs = await get_wikibase_list_with_out_of_date_stats_observations()
    for wikibase in ood_stats_obs:
        try:
            await create_special_statistics_observation(wikibase.id)
        except:
            pass


async def update_out_of_date_user_observations():
    """Update Out of Date User Observations"""

    ood_user_obs = await get_wikibase_list_with_out_of_date_user_observations()
    for wikibase in ood_user_obs:
        await create_user_observation(wikibase.id)
