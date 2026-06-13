import asyncio
import time

from langame_api import get_pc_linking

PC_MONITOR = {}


def get_monitor_status(uuid):

    if uuid not in PC_MONITOR:

        return "shutdown"

    return PC_MONITOR[uuid]["status"]


async def monitor_pcs():

    while True:

        try:

            data = get_pc_linking()

            for pc in data["data"]:

                uuid = pc["UUID"]

                PC_MONITOR[uuid] = {
                    "status": "free",
                    "last_seen": time.time()
                }

            print("ПК в памяти:", len(PC_MONITOR))

        except Exception as e:

            print("ОШИБКА МОНИТОРА:", e)

        await asyncio.sleep(5)
