from ota import *
from cricket import *

print("PEANUTS")

async def main():
    asyncio.create_task(start_ota())
    await Cricket().run()

asyncio.run(main())
