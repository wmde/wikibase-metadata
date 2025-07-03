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
