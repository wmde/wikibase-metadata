"""Test Data Expectations with Great Expectations"""

import os
from pathlib import Path
import sys
from typing import List
from great_expectations.data_context import FileDataContext

GREAT_EXPECTATIONS_PROJECT_ROOT = "./data"
CHECKPOINT_DIRECTORY = "./data/gx/checkpoints"


# Define the pytest_generate_tests hook to generate test cases
def pytest_generate_tests(metafunc):
    """Add Parameters"""
    checkpoints = [Path(file).stem for file in os.listdir(CHECKPOINT_DIRECTORY)]

    if "checkpoint_name" in metafunc.fixturenames:
        # Generate test cases based on the test_data list
        metafunc.parametrize("checkpoint_name", sorted(checkpoints))


def test_data_expectations(checkpoint_name: str):
    """Test Data Expectations with Great Expectations"""

    print(f"\n{checkpoint_name}")
    context = FileDataContext(project_root_dir=GREAT_EXPECTATIONS_PROJECT_ROOT)
    retrieved_checkpoint = context.get_checkpoint(name=checkpoint_name)
    result = retrieved_checkpoint.run()
    assert result.success, result.run_results

    context.build_data_docs()


if __name__ == "__main__":
    SUCCESS = True
    check_list: List[str]
    if len(sys.argv) < 2:
        check_list = [Path(file).stem for file in os.listdir(CHECKPOINT_DIRECTORY)]
    else:
        check_list = sys.argv[1:]

    for check in sorted(check_list):
        print(check)
        try:
            test_data_expectations(checkpoint_name=check)
        except AssertionError:
            SUCCESS = False

    assert SUCCESS
