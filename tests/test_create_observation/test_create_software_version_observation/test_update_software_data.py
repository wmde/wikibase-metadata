"""Test Extension Data"""

from datetime import datetime

from freezegun import freeze_time
import pytest

from fetch_data import get_update_extension_query, update_software_data
from tests.test_create_observation.test_create_software_version_observation.test_constants import (
    DATA_DIRECTORY,
)
from tests.utils import MockResponse


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="update-software-data",
    depends=["software-version-success", "merge-software-by-id"],
    scope="session",
)
@pytest.mark.version
async def test_update_software_data(mocker):
    """Test Update Software Data"""

    # pylint: disable-next=unused-argument,too-many-return-statements
    def mockery(*args, **kwargs):
        assert kwargs.get("timeout") == 10
        query = args[0]
        match query:
            # Babel
            case "https://www.mediawiki.org/wiki/Extension:Babel":
                with open(f"{DATA_DIRECTORY}/Mediawiki_Babel.html", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            # Google Analytics Integration - redirect
            case (
                "https://www.mediawiki.org/wiki/Extension:Google Analytics Integration"
            ):
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_GoogleAnalyticsIntegration.html",
                    mode="rb",
                ) as data:
                    return MockResponse(
                        "https://www.mediawiki.org/wiki/Extension:Google_Analytics_Integration",
                        200,
                        data.read(),
                    )
            # Labeled Section Transclusion - redirect
            case "https://www.mediawiki.org/wiki/Extension:LabeledSectionTransclusion":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_LabeledSectionTransclusion.html",
                    mode="rb",
                ) as data:
                    return MockResponse(
                        "https://www.mediawiki.org/wiki/Extension:Labeled_Section_Transclusion",
                        200,
                        data.read(),
                    )
            # Miraheze Magic - 404
            case "https://www.mediawiki.org/wiki/Extension:MirahezeMagic":
                return MockResponse(
                    "https://www.mediawiki.org/wiki/Extension:MirahezeMagic", 404
                )
            # Proofread Page - redirect
            case "https://www.mediawiki.org/wiki/Extension:ProofreadPage":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_ProofreadPage.html", mode="rb"
                ) as data:
                    return MockResponse(
                        "https://www.mediawiki.org/wiki/Extension:Proofread_Page",
                        200,
                        data.read(),
                    )
            # Scribunto
            case "https://www.mediawiki.org/wiki/Extension:Scribunto":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_Scribunto.html", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
            # Universal Language Selector
            case "https://www.mediawiki.org/wiki/Extension:UniversalLanguageSelector":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_UniversalLanguageSelector.html",
                    mode="rb",
                ) as data:
                    return MockResponse(query, 200, data.read())
            # Wikibase Client - redirect
            case "https://www.mediawiki.org/wiki/Extension:WikibaseClient":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_WikibaseClient.html", mode="rb"
                ) as data:
                    return MockResponse(
                        "https://www.mediawiki.org/wiki/Extension:Wikibase_Client",
                        200,
                        data.read(),
                    )
            # Wikibase Lib - Arcived - redirect to permalink
            case "https://www.mediawiki.org/wiki/Extension:WikibaseLib":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_WikibaseLib.html", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
            # Wikibase Repository - redirect
            case "https://www.mediawiki.org/wiki/Extension:WikibaseRepository":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_WikibaseRepository.html", mode="rb"
                ) as data:
                    return MockResponse(
                        "https://www.mediawiki.org/wiki/Extension:Wikibase_Repository",
                        200,
                        data.read(),
                    )
            # Wikibase View
            case "https://www.mediawiki.org/wiki/Extension:WikibaseView":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_WikibaseView.html", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
            # Wikibase Lib Archived Page
            case "https://www.mediawiki.org/wiki/Special:PermanentLink/3981869":
                with open(
                    f"{DATA_DIRECTORY}/Mediawiki_WikibaseLib_Archived.html", mode="rb"
                ) as data:
                    return MockResponse(
                        "https://www.mediawiki.org/w/index.php?oldid=3981869",
                        200,
                        data.read(),
                    )
        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.soup_data.software.get_update_software_data.requests.get",
        side_effect=mockery,
    )

    await update_software_data()


@pytest.mark.version
def test_get_update_extension_query():
    """Test Update Extension Query"""

    query = get_update_extension_query()
    assert str(query) == (
        # pylint: disable=line-too-long
        """SELECT wikibase_software.id, wikibase_software.software_type, wikibase_software.software_name, wikibase_software.url, wikibase_software.fetched, wikibase_software.description, wikibase_software.latest_version, wikibase_software.quarterly_download_count, wikibase_software.public_wiki_count, wikibase_software.mw_bundled, wikibase_software.wbs_bundled, wikibase_software.archived 
FROM wikibase_software 
WHERE (wikibase_software.fetched IS NULL OR wikibase_software.fetched < :fetched_1) AND wikibase_software.software_type = :software_type_1 AND (wikibase_software.archived = false OR wikibase_software.archived IS NULL)
 LIMIT :param_1"""
    )
