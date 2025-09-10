# Metrics CSV

1 row per Wikibase, with the following columns:

- `wikibase_id`
  - internal identifier
  - automatically assigned upon adding to database
- `wikibase_type`
  - manually set
  - CSV excludes TEST wikibases
- `base_url`
  - manually set

From latest successful Quantity observation:

- `quantity_observation_date`
  - date of quantity observation
  - automatically set when Scraper attempts to fetch data
- `total_items`
  - SPARQL query
  - Number of Wikibase items in database
- `total_lexemes`
  - SPARQL query
  - Number of Wikibase lexemes in database
- `total_properties`
  - SPARQL query
  - Number of properties in database
- `total_triples`
  - SPARQL query
  - Number of triples in database

From latest successful External Identifier observation:

- `ei_observation_date`
  - date of external identifier observation
  - automatically set when Scraper attempts to fetch data
- `total_ei_properties`
  - SPARQL query
  - Number of external identifier properties in database
- `total_ei_statements`
  - SPARQL query
  - Number of external identifier statements in database
- `total_url_properties`
  - SPARQL query
  - Number of url properties in database
- `total_url_statements`
  - SPARQL query
  - Number of url statements in database

From latest successful Recent Changes observation:

- `recent_changes_observation_date`
  - date of recent changes observation
  - automatically set when Scraper attempts to fetch data
- `first_change_date`
  - oldest record in recent changes list (limited to 30 days before observation date)
  - pulled from action api
- `last_change_date`
  - newest record in recent changes list (limited as above)
  - pulled from action api
- `human_change_count`
  - number of records in recent changes list (limited as above), excluding bot contributions
  - pulled from action api
- `human_change_user_count`
  - number of distinct users with at least one record in recent changes list (limited as above), excluding bot contributions
  - pulled from action api
- `human_change_active_user_count`
  - number of distinct users with at least five records in recent changes list (limited as above), excluding bot contributions
  - pulled from action api
- `bot_change_count`
  - number of records in recent changes list (limited as above), limited to bot contributions
  - pulled from action api
- `bot_change_user_count`
  - number of distinct users with at least one record in recent changes list (limited as above), limited to bot contributions
  - pulled from action api
- `bot_change_active_user_count`
  - number of distinct users with at least five records in recent changes list (limited as above), limited to bot contributions
  - pulled from action api

From latest successful Software Version observation:

- `software_version_observation_date`
  - date of software version observation
  - automatically set when Scraper attempts to fetch data
- `software_name`
  - ONLY MediaWiki
- `version`
  - MediaWiki version
  - Scraped from Special:Version page
