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
    create_software_version_observation_without_background_task,
    create_special_statistics_observation,
)
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)
from fetch_data.cloud_api_data import (
    update_cloud_instances,
)
from logger import logger


async def update_out_of_date_connectivity_observations():
    """Update Out of Date Connectivity Observations"""

    ood_con_obs = await get_wikibase_list_with_out_of_date_connectivity_observations()
    logger.info(f"Connectivity: {len(ood_con_obs)} Wikibases to Update")
    for wikibase in ood_con_obs:
        try:
            await create_connectivity_observation(wikibase.id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "ConnectivityDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_log_first_observations():
    """Update Out of Date Log (First Month) Observations"""

    ood_log_obs = await get_wikibase_list_with_out_of_date_log_first_observations()
    logger.info(f"Log (First Month): {len(ood_log_obs)} Wikibases to Update")
    for wikibase in ood_log_obs:
        try:
            await create_log_observation(wikibase.id, first_month=True)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "LogDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_log_last_observations():
    """Update Out of Date Log (Last Month) Observations"""

    ood_log_obs = await get_wikibase_list_with_out_of_date_log_last_observations()
    logger.info(f"Log (Last Month): {len(ood_log_obs)} Wikibases to Update")
    for wikibase in ood_log_obs:
        try:
            await create_log_observation(wikibase.id, first_month=False)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "LogDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_property_observations():
    """Update Out of Date Property Popularity Observations"""

    ood_prop_obs = (
        await get_wikibase_list_with_out_of_date_property_popularity_observations()
    )
    logger.info(f"Property Popularity: {len(ood_prop_obs)} Wikibases to Update")
    for wikibase in ood_prop_obs:
        try:
            await create_property_popularity_observation(wikibase.id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "PropertyPopularityDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_quantity_observations():
    """Update Out of Date Quantity Observations"""

    ood_quant_obs = await get_wikibase_list_with_out_of_date_quantity_observations()
    logger.info(f"Quantity: {len(ood_quant_obs)} Wikibases to Update")
    for wikibase in ood_quant_obs:
        try:
            await create_quantity_observation(wikibase.id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "QuantityDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_software_observations():
    """Update Out of Date Software Version Observations"""

    ood_soft_obs = await get_wikibase_list_with_out_of_date_software_observations()
    logger.info(f"Software Version: {len(ood_soft_obs)} Wikibases to Update")
    for wikibase in ood_soft_obs:
        try:
            await create_software_version_observation_without_background_task(
                wikibase.id
            )
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "SoftwareVersionDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_stats_observations():
    """Update Out of Date Special:Statistics Observations"""

    ood_stats_obs = await get_wikibase_list_with_out_of_date_stats_observations()
    logger.info(f"Statistics: {len(ood_stats_obs)} Wikibases to Update")
    for wikibase in ood_stats_obs:
        try:
            await create_special_statistics_observation(wikibase.id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "StatisticsDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_user_observations():
    """Update Out of Date User Observations"""

    ood_user_obs = await get_wikibase_list_with_out_of_date_user_observations()
    logger.info(f"User: {len(ood_user_obs)} Wikibases to Update")
    for wikibase in ood_user_obs:
        try:
            await create_user_observation(wikibase.id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "UserDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )


async def update_out_of_date_cloud_instances():
    """Pull cloud instaces and update our local database"""

    logger.info("Pulling cloud instances and updating local database")
    try:
        await update_cloud_instances()
    # pylint: disable-next=bare-except
    except:
        logger.error(
            "CloudInstancesError",
            exc_info=True,
            stack_info=True,
        )
