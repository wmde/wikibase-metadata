"""Result of Bulk Task Work"""

import asyncio
import strawberry


@strawberry.type
class BulkTaskResult:
    """Result of Bulk Task Execution"""

    success: int
    failure: int
    total: int

    def __init__(self, tasks: list[asyncio.Task[bool]]):
        self.success = len([t for t in tasks if t.result()])
        self.failure = len([t for t in tasks if not t.result()])
        self.total = len(tasks)
