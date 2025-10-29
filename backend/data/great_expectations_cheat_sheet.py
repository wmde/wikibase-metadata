"""Example code adding new expectations to Great Expectations"""

# python data/great_expectations_cheat_sheet.py

import great_expectations as gx
from great_expectations import expectations as gxe

ROOT = "./data"
context = gx.get_context(project_root_dir=ROOT)
data_source = context.data_sources.get("wikibase_datasource")

# Add Columns to Existing Suites:
suite = context.suites.get(name="wikibase_quantity_observation_expectation_suite")
suite.expectations.append(
    gxe.ExpectColumnToExist(column="total_external_identifier_properties")
)
suite.expectations.append(
    gxe.ExpectColumnToExist(column="total_external_identifier_statements")
)
suite.expectations.append(gxe.ExpectColumnToExist(column="total_url_properties"))
suite.expectations.append(gxe.ExpectColumnToExist(column="total_url_statements"))
suite.save()


valid_suite = context.suites.get(
    name="valid_wikibase_quantity_observation_expectation_suite"
)
# valid_suite.expectations.append(
#     gxe.ExpectColumnValuesToNotBeNull(column="total_external_identifier_properties")
# )
valid_suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(
        column="total_external_identifier_properties", min_value=0
    )
)
valid_suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(
        column="total_external_identifier_statements", min_value=0
    )
)
valid_suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(column="total_url_properties", min_value=0)
)
valid_suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(column="total_url_statements", min_value=0)
)
valid_suite.save()


# Add Observation Table
tda = data_source.add_table_asset(
    table_name="wikibase_external_identifier_observation",
    name="wikibase_external_identifier_observation_table",
)
bd = tda.add_batch_definition_whole_table(name="FULL_TABLE")
qa = data_source.add_query_asset(
    query="SELECT * FROM wikibase_external_identifier_observation WHERE anything",
    name="valid_wikibase_external_identifier_observation",
)
valid_bd = qa.add_batch_definition_whole_table(name="FULL_TABLE")

obs_suite = context.suites.get(name="wikibase_observation_expectation_suite")
obs_vd = gx.ValidationDefinition(
    data=bd,
    suite=obs_suite,
    name="obs_wikibase_external_identifier_observation_validation_definition",
)
context.validation_definitions.add(obs_vd)

wikibase_checkpoint = context.checkpoints.get("wikibase_checkpoint")
context.checkpoints.add(
    checkpoint := gx.Checkpoint(
        name="wikibase_external_identifier_observation_checkpoint",
        validation_definitions=[obs_vd],
        actions=wikibase_checkpoint.actions,
        result_format={"result_format": "COMPLETE"},
    )
)

table_suite = gx.ExpectationSuite(
    name="wikibase_external_identifier_observation_expectation_suite"
)
context.suites.add(table_suite)
# Add Expectations
table_suite.save()
table_vd = gx.ValidationDefinition(
    data=bd,
    suite=table_suite,
    name="wikibase_external_identifier_observation_validation_definition",
)
context.validation_definitions.add(table_vd)
checkpoint.validation_definitions.append(table_vd)
checkpoint.save()

valid_suite = gx.ExpectationSuite(
    name="valid_wikibase_external_identifier_observation_expectation_suite"
)
context.suites.add(valid_suite)
# Add Expectations
valid_suite.save()
valid_vd = gx.ValidationDefinition(
    data=valid_bd,
    suite=valid_suite,
    name="valid_wikibase_external_identifier_observation_validation_definition",
)
context.validation_definitions.add(valid_vd)
checkpoint.validation_definitions.append(valid_vd)
checkpoint.save()
