"""Example code adding new expectations to Great Expectations"""

# python data/great_expectations_cheat_sheet.py

import great_expectations as gx
from great_expectations import expectations as gxe

ROOT = "./data"
context = gx.get_context(project_root_dir=ROOT)
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
# valid_suite.expectations.append(gx.expectations.ExpectColumnValuesToNotBeNull(column='total_external_identifier_properties'))
valid_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_external_identifier_properties", min_value=0
    )
)
valid_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_external_identifier_statements", min_value=0
    )
)
valid_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_url_properties", min_value=0
    )
)
valid_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_url_statements", min_value=0
    )
)
valid_suite.save()
