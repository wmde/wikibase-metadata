"""Create API Quantity Observation"""

from http.client import IncompleteRead
from json import JSONDecodeError

from requests.exceptions import (
    ChunkedEncodingError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
)
from urllib3.exceptions import (
    ConnectTimeoutError,
    MaxRetryError,
    NameResolutionError,
    ProtocolError,
)

from data import get_async_session
from fetch_data.api_data.api_quantity.fetch_total_page_count import (
    fetch_total_page_count,
)
from fetch_data.api_data.util import get_namespaces, parse_namespace
from fetch_data.utils import get_wikibase_from_database
from logger import logger
from model.database import WikibaseAPIQuantityObservationModel, WikibaseModel


async def create_api_quantity_observation(wikibase_id: int):
    """Create API Quantity Observation"""

    logger.debug(
        "API Quantity: Attempting Observation", extra={"wikibase": wikibase_id}
    )

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_api_quantity_observations=True,
            require_script_path=True,
        )

        observation = WikibaseAPIQuantityObservationModel(wikibase_id=wikibase.id)

        try:
            namespaces = await get_namespaces(api_url=wikibase.action_api_url())

            item_namespace_id = parse_namespace(
                namespaces, prop="defaultcontentmodel", value="wikibase-item"
            )
            if item_namespace_id is not None:
                observation.total_items = await fetch_total_page_count(
                    api_url=wikibase.action_api_url(), namespace_id=item_namespace_id
                )
                observation.returned_data = True

            lexeme_namespace_id = parse_namespace(
                namespaces, prop="defaultcontentmodel", value="wikibase-lexeme"
            )
            if lexeme_namespace_id is not None:
                observation.total_lexemes = await fetch_total_page_count(
                    api_url=wikibase.action_api_url(), namespace_id=lexeme_namespace_id
                )
                observation.returned_data = True

            property_namespace_id = parse_namespace(
                namespaces, prop="defaultcontentmodel", value="wikibase-property"
            )
            if property_namespace_id is not None:
                observation.total_properties = await fetch_total_page_count(
                    api_url=wikibase.action_api_url(),
                    namespace_id=property_namespace_id,
                )
                observation.returned_data = True

        except (
            ConnectTimeoutError,
            ConnectionError,
            MaxRetryError,
            NameResolutionError,
            ReadTimeout,
            SSLError,
            TooManyRedirects,
        ):
            logger.error("SuspectWikibaseOfflineError", extra={"wikibase": wikibase.id})
            observation.returned_data = False

        except (ChunkedEncodingError, IncompleteRead, JSONDecodeError, ProtocolError):
            logger.warning("APIQuantityDataError", extra={"wikibase": wikibase.id})
            observation.returned_data = False

        wikibase.api_quantity_observations.append(observation)

        await async_session.commit()

        logger.debug(
            "API Quantity: Observation returned data: "
            + str(observation.returned_data),
            extra={"wikibase": wikibase_id},
        )
        return observation.returned_data
