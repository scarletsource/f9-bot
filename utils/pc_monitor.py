import asyncio
import time

from langame_api import (
    get_pc_linking,
    get_busy_pcs
)

PC_MONITOR = {}


def get_monitor_status(uuid):

    if uuid not in PC_MONITOR:

        return "shutdown"

    return PC_MONITOR[uuid]["status"]


async def monitor_pcs():

    while True:

        try:

            data = get_pc_linking()

            busy_pcs = get_busy_pcs()

            print()
            print("ЗАНЯТЫЕ ПК:")

            for uuid in busy_pcs:

                print(uuid)

            print()

            for pc in data["data"]:

                uuid = pc["UUID"]

                status = "free"

                if uuid in busy_pcs:

                    status = "session"

                PC_MONITOR[uuid] = {

                    "pc_name": pc["name"],

                    "fiscal_name": pc["fiscal_name"],

                    "guest_id": None,

                    "status": status,

                    "last_seen": time.time()
                }

            sessions = sum(
                1
                for pc in PC_MONITOR.values()
                if pc["status"] == "session"
            )

            print(
                f"ПК в памяти: {len(PC_MONITOR)} | "
                f"На сессии: {sessions}"
            )

            print()
            print("МОНИТОР:")

            for uuid, pc in PC_MONITOR.items():

                print(
                    pc["pc_name"],
                    "|",
                    pc["fiscal_name"],
                    "|",
                    pc["status"]
                )

            print()

        except Exception as e:

            print(
                "ОШИБКА МОНИТОРА:",
                e
            )

        await asyncio.sleep(5)
