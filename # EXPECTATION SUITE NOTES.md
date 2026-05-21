# EXPECTATION SUITE NOTES

nonzero_wikibase_log_observation_month_expectation_suite.json
- user_count_no_bot: expect_column_values_to_not_be_null: 100% -> 98%
    - Constructor should never result in null value
    - 1 record fits the bill - `anything` is false, and it appears to have crashed on the `active_user_count` step
    - Suggest: further filter query to `anything` is true, reset expection to 100%

populated_wikibase_software_expectation_suite.json
- description: expect_column_values_to_not_be_null: 70% -> 55%
    - Per spot-checking, several instances have url but no other data, and webpages do have no text. However, some have latest_version data but not descriptions, and websites do appear to have description text. Suggest: periodic re-fetch expectations that have no descriptions but have other data, investigate fetcher for proper description parsing
- latest_version: expect_column_values_to_not_be_null: 60% -> 49%
    - Per spot-checking: several instances legit do not have this datum. Remove expectation
- quarterly_download_count: expect_column_values_to_not_be_null: 25% -> 0.1%
    - Per spot-checking: several instances legit do not have this datum. Remove expectation
- public_wiki_count: expect_column_values_to_not_be_null: 25% -> 0.1%
    - Per spot-checking: several instances legit do not have this datum. Remove expectation
- mw_bundled: expect_column_values_to_not_be_null: 75% -> 57%
    - Found 1 record where not archived and mw_bundled null
- archived: expect_column_values_to_not_be_null: 75% -> 57%
    - Per spot-checking: several instances have entirely blank pages
- Suggest: move all criteria except archived to another validation definition that also filters on not archived

valid_wikibase_external_identifier_observation_expectation_suite.json
- total_external_identifier_properties: min_value: 1 -> 0
    - Valid
- total_external_identifier_statements: min_value: 1 -> 0
    - Valid
- total_url_properties: min_value: 1 -> 0
    - Valid
- total_url_statements: min_value: 1 -> 0
    - Valid

valid_wikibase_quantity_observation_expectation_suite.json
- total_items: min_value: 1 -> 0
    - Valid - though, check if instances are actual Wikibases
- total_properties: min_value: 1 -> 0
    - Valid - though, check if instances are actual Wikibases
- total_triples: min_value: 1 -> 0
    - Valid - though, check if instances are actual Wikibases

wikibase_expectation_suite.json
- wikibase_name: whitespace: 100% -> 97%
    - Could not find any such records
    - Reset expectation to 100%
- wb_type: expect_column_distinct_values_to_be_in_set: add TEST
    - VALID

wikibase_log_observation_month_type_expectation_suite.json
- log_type: expect_column_distinct_values_to_be_in_set: add PAGE_TRANSLATE_REVIEW, UNCLASSIFIED, USER_UNBLOCK
    - VALID

wikibase_url_expectation_suite.json
- url: whitespace: removed
    - Replaced by below: VALID

wikibase_url_full_expectation_suite.json
- created - VALID

wikibase_url_path_expectation_suite.json
- created - VALID

