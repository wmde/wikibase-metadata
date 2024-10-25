"""MockInfo"""

from typing import List


class MockBackgroundClassList:
    """Mock Backround Class List"""

    tasks: List

    def add_task(self, task):
        """Add Background Task"""

        self.tasks.append(task)

    def __init__(self):
        self.tasks = []


class MockInfo:
    """Mock StrawberryInfo"""

    context: dict

    def __init__(self, context: dict):
        self.context = context
