"""Pull Wikibase Data"""

import asyncio
import json

from sqlalchemy import or_, select
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_url_model import WikibaseURLModel

WIKIBASES_QUERY = """PREFIX wdt: <https://wikibase.world/prop/direct/>
PREFIX wd: <https://wikibase.world/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
SELECT ?itemLabel ?url ?host ?hostLabel ?available ?availableLabel ?sparqlUIUrl ?sparqlEndpointUrl WHERE {
  ?item wdt:P3 wd:Q10;
    wdt:P1 ?url;
    wdt:P2 ?host;
    wdt:P13 ?available.
#   FILTER(?host != wd:Q4)
#   FILTER(?host != wd:Q6)
#   FILTER(?host != wd:Q7)
#   FILTER(?host != wd:Q117)
#   FILTER(?host != wd:Q8)
  OPTIONAL { ?item wdt:P7 ?sparqlUIUrl. }
  OPTIONAL { ?item wdt:P8 ?sparqlEndpointUrl. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}"""


async def pull_wikibase_world():
    """Pull Wikibase Data"""
    # data = get_results(
    #     endpoint_url="https://wikibase.world/query/sparql",
    #     query=WIKIBASES_QUERY,
    #     query_name="Pull Wikibases",
    # )
    # print(data)

    with open(
        "./data/wikibase_world_data.json", mode="r", encoding="utf-8"
    ) as data_file:
        data = json.loads(data_file.read())
        async with get_async_session() as async_session:

            for record in data:
                existing = (
                    await async_session.scalars(
                        select(WikibaseModel).where(
                            or_(
                                WikibaseModel.wikibase_name == record.get("itemLabel"),
                                WikibaseModel.url.has(
                                    WikibaseURLModel.url == record.get("url")
                                ),
                            )
                        )
                    )
                ).all()
                if len(existing) == 0:
                    print(record.get("itemLabel"))
                    async_session.add(
                        WikibaseModel(
                            wikibase_name=record.get("itemLabel"),
                            base_url=record.get("url"),
                            sparql_query_url=record.get("sparqlUIUrl"),
                            sparql_endpoint_url=record.get("sparqlEndpointUrl"),
                            region="",
                        )
                    )
            await async_session.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(pull_wikibase_world())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
