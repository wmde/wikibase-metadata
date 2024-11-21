"""Check Out of Date Observations"""

import asyncio

from fetch_data import (
    get_wikibase_list_with_out_of_date_connectivity_observations,
    get_wikibase_list_with_out_of_date_log_first_observations,
    get_wikibase_list_with_out_of_date_log_last_observations,
    get_wikibase_list_with_out_of_date_property_popularity_observations,
    get_wikibase_list_with_out_of_date_quantity_observations,
    get_wikibase_list_with_out_of_date_software_observations,
    get_wikibase_list_with_out_of_date_stats_observations,
    get_wikibase_list_with_out_of_date_user_observations,
)
from logger import logger


async def check_out_of_date():
    """Print Number of Out of Date Observations"""

    ood_con_obs = await get_wikibase_list_with_out_of_date_connectivity_observations()
    logger.info(f"Connectivity: {len(ood_con_obs)}")

    ood_log_first_obs = (
        await get_wikibase_list_with_out_of_date_log_first_observations()
    )
    logger.info(f"Logs (First): {len(ood_log_first_obs)}")

    ood_log_last_obs = await get_wikibase_list_with_out_of_date_log_last_observations()
    logger.info(f"Logs (Last): {len(ood_log_last_obs)}")

    ood_prop_obs = (
        await get_wikibase_list_with_out_of_date_property_popularity_observations()
    )
    logger.info(f"Property: {len(ood_prop_obs)}")

    ood_quant_obs = await get_wikibase_list_with_out_of_date_quantity_observations()
    logger.info(f"Quantity: {len(ood_quant_obs)}")

    ood_soft_obs = await get_wikibase_list_with_out_of_date_software_observations()
    logger.info(f"Software: {len(ood_soft_obs)}")

    ood_stats_obs = await get_wikibase_list_with_out_of_date_stats_observations()
    logger.info(f"Statistics: {len(ood_stats_obs)}")

    ood_user_obs = await get_wikibase_list_with_out_of_date_user_observations()
    logger.info(f"User: {len(ood_user_obs)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(check_out_of_date())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
