import asyncio
from functools import partial

from .core import create_scheduler, health_handler


async def main():
    """Create and run the scheduler server"""
    scheduler = create_scheduler()
    scheduler.start()

    server = await asyncio.start_server(
        partial(health_handler, scheduler=scheduler),
        "0.0.0.0",
        8001,
    )

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
