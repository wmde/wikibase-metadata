"""Test Data Expectations with Great Expectations"""

import os
import pytest
import great_expectations as gx

GREAT_EXPECTATIONS_PROJECT_ROOT = "./data"
CHECKPOINT_DIRECTORY = "./data/gx/checkpoints"


# Define the pytest_generate_tests hook to generate test cases
def pytest_generate_tests(metafunc):
    """Add Parameters"""

    if "checkpoint_name" in metafunc.fixturenames:
        # Generate test cases based on the test_data list
        metafunc.parametrize(
            "checkpoint_name", sorted(os.listdir(CHECKPOINT_DIRECTORY))
        )


@pytest.mark.data
def test_data_expectations(checkpoint_name: str):
    """Test Data Expectations with Great Expectations"""

    print(f"\n{checkpoint_name}")
    context = gx.get_context(project_root_dir=GREAT_EXPECTATIONS_PROJECT_ROOT)
    retrieved_checkpoint = context.checkpoints.get(checkpoint_name)
    result = retrieved_checkpoint.run()
    assert result.success, result.run_results

    context.build_data_docs()
