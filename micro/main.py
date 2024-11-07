from monitor import *
from cricket import *


async def main():
    asyncio.create_task(start_monitor())
    await Cricket().run()

asyncio.run(main())
