import asyncio

async def monitor_pcs():

    while True:

        print("МОНИТОР ОБНОВИЛСЯ")

        await asyncio.sleep(5)
