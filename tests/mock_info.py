"""MockInfo"""


class MockBackgroundClassList:
    """Mock Backround Class List"""

    tasks: list

    def add_task(self, task):
        self.tasks.append(task)

    def __init__(self):
        self.tasks = []


class MockInfo:
    """Mock StrawberryInfo"""

    context: dict

    def __init__(self, context: dict):
        self.context = context
