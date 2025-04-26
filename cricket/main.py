from ota import *
from cricket import *


async def main():
    asyncio.create_task(start_ota(cricket))
    await cricket.run()


cricket = Cricket()
asyncio.run(main())

