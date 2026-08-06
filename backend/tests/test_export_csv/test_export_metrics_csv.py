"""Test Export Metrics CSV"""

from datetime import datetime, timezone
import re
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from export_csv.metric import export_metric_csv
from model.database.wikibase_observation.external_identifier.wikibase_ei_obs_model import (
    WikibaseExternalIdentifierObservationModel,
)
from model.database.wikibase_observation.quantity.wikibase_quantity_observation_model import (
    WikibaseQuantityObservationModel,
)
from model.database.wikibase_observation.recent_changes.recent_changes_observation_model import (
    WikibaseRecentChangesObservationModel,
)
from model.database.wikibase_observation.version.software_version_model import (
    WikibaseSoftwareVersionModel,
)
from model.database.wikibase_observation.version.wikibase_version_observation_model import (
    WikibaseSoftwareVersionObservationModel,
)
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum import WikibaseType, WikibaseSoftwareType

from model.database import WikibaseModel

EXPECTED_HEADER_ROW = ",".join(
    [
        "wikibase_id",
        "wikibase_type",
        "reuse",
        "base_url",
        "quantity_observation_date",
        "total_items",
        "total_lexemes",
        "total_properties",
        "total_triples",
        "ei_observation_date",
        "total_ei_properties",
        "total_ei_statements",
        "total_url_properties",
        "total_url_statements",
        "recent_changes_observation_date",
        "first_change_date",
        "last_change_date",
        "human_change_count",
        "human_change_user_count",
        "human_change_active_user_count",
        "bot_change_count",
        "bot_change_user_count",
        "bot_change_active_user_count",
        "software_version_observation_date",
        "software_name",
        "version",
        "manifest",
    ]
)
EXPECTED_PATTERN_LIST = [
    re.compile(r"\d+"),
    re.compile(r"(WikibaseType\.(CLOUD|OTHER|SUITE)|)"),
    re.compile(r"(True|False|)"),
    re.compile(r"https?://[a-z0-9\-_.\?=/]+"),
    # Quantity
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    # External Identifier
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    # # Recent Changes
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    # # Software
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(MediaWiki|)"),
    re.compile(r"(\d+\.\d+\.\d+|)"),
    re.compile(r"(True|False)"),
]


@pytest.fixture
async def wikibases(db_session):  # pylint: disable=too-many-locals, too-many-statements
    """Create 3 wikibases for CSV export tests"""
    wikibase_ids = []
    async with AsyncSession(bind=db_session) as session:
        types = [WikibaseType.CLOUD, WikibaseType.OTHER, WikibaseType.SUITE]
        for i, wikibase_type in enumerate(types):
            wikibase = WikibaseModel(
                wikibase_name=f"CSV Export Test Wikibase {i}",
                base_url=f"https://csv-export-example-{i}.com",
                reuse=True,
                wikibase_type=wikibase_type,
            )
            wikibase.checked = True
            session.add(wikibase)
            await session.flush()
            await session.refresh(wikibase)
            wikibase_ids.append(wikibase.id)

        primary_wikibase_id = wikibase_ids[0]

        quantity_obs = WikibaseQuantityObservationModel()
        quantity_obs.wikibase_id = primary_wikibase_id
        quantity_obs.returned_data = True
        quantity_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        quantity_obs.total_items = 100
        quantity_obs.total_lexemes = 10
        quantity_obs.total_properties = 20
        quantity_obs.total_triples = 500
        session.add(quantity_obs)

        ei_obs = WikibaseExternalIdentifierObservationModel()
        ei_obs.wikibase_id = primary_wikibase_id
        ei_obs.returned_data = True
        ei_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        ei_obs.total_external_identifier_properties = 5
        ei_obs.total_external_identifier_statements = 50
        ei_obs.total_url_properties = 3
        ei_obs.total_url_statements = 30
        session.add(ei_obs)

        rc_obs = WikibaseRecentChangesObservationModel()
        rc_obs.wikibase_id = primary_wikibase_id
        rc_obs.returned_data = True
        rc_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        rc_obs.first_change_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        rc_obs.last_change_date = datetime(2024, 3, 5, tzinfo=timezone.utc)
        rc_obs.human_change_count = 10
        rc_obs.human_change_user_count = 5
        rc_obs.human_change_active_user_count = 1
        rc_obs.bot_change_count = 6
        rc_obs.bot_change_user_count = 2
        rc_obs.bot_change_active_user_count = 1
        session.add(rc_obs)

        mediawiki_software = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.SOFTWARE,
            software_name="MediaWiki",
        )
        session.add(mediawiki_software)
        await session.flush()

        manifest_software = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseManifest",
        )
        session.add(manifest_software)
        await session.flush()

        sv_obs = WikibaseSoftwareVersionObservationModel()
        sv_obs.wikibase_id = primary_wikibase_id
        sv_obs.returned_data = True
        sv_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(sv_obs)
        await session.flush()
        await session.refresh(sv_obs)

        mediawiki_version = WikibaseSoftwareVersionModel(
            software=mediawiki_software,
            version="1.39.8",
        )
        mediawiki_version.wikibase_software_version_observation_id = sv_obs.id
        session.add(mediawiki_version)

        manifest_version = WikibaseSoftwareVersionModel(
            software=manifest_software,
            version="1.0.0",
        )
        manifest_version.wikibase_software_version_observation_id = sv_obs.id
        session.add(manifest_version)

        await session.flush()

    return wikibase_ids


@pytest.mark.asyncio
async def test_export_metric_csv(
    wikibases,
    db_session,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Export Metric CSV"""

    response = await export_metric_csv(connection=db_session)
    content = response.body.decode("utf-8")

    lines = content.splitlines()
    assert len(lines) == 4  # header + 3 wikibases
    assert lines[0] == EXPECTED_HEADER_ROW

    for line in lines[1:]:
        for i, pattern in enumerate(EXPECTED_PATTERN_LIST):
            assert pattern.match(line.split(",")[i])
