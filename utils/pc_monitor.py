import asyncio
import time

from langame_api import (
    get_pc_linking,
    get_guest_sessions
)

PC_MONITOR = {}

def get_monitor_status(uuid):

    if uuid not in PC_MONITOR:

        return "shutdown"

    return PC_MONITOR[uuid]["status"]


def get_monitor_name(uuid):

    if uuid not in PC_MONITOR:

        return "Неизвестно"

    return PC_MONITOR[uuid]["pc_name"]


def get_monitor_fiscal_name(uuid):

    if uuid not in PC_MONITOR:

        return "-"

    return PC_MONITOR[uuid]["fiscal_name"]


def get_monitor_guest(uuid):

    if uuid not in PC_MONITOR:

        return None

    return PC_MONITOR[uuid]["guest_id"]


async def monitor_pcs():

    while True:

        try:

            data = get_pc_linking()

            sessions_data = get_guest_sessions()

            # сбрасываем статусы
            for uuid in PC_MONITOR:

                PC_MONITOR[uuid]["status"] = "free"
                PC_MONITOR[uuid]["guest_id"] = None
                PC_MONITOR[uuid]["date_start"] = None

            # обновляем список ПК
            for pc in data["data"]:

                uuid = pc["UUID"]

                if uuid not in PC_MONITOR:

                    PC_MONITOR[uuid] = {

                        "pc_name": pc["name"],

                        "fiscal_name": pc["fiscal_name"],

                        "guest_id": None,

                        "date_start": None,

                        "status": "free",

                        "last_seen": time.time()
                    }

                else:

                    PC_MONITOR[uuid]["last_seen"] = time.time()

            # отмечаем активные сессии
            for session in sessions_data["data"]:

                if session["date_stop"] is not None:
                    continue

                uuid = session["UUID"]

                if uuid not in PC_MONITOR:
                    continue

                PC_MONITOR[uuid]["status"] = "session"

                PC_MONITOR[uuid]["guest_id"] = session["guest_id"]

                PC_MONITOR[uuid]["date_start"] = session["date_start"]

            sessions_count = sum(
                1
                for pc in PC_MONITOR.values()
                if pc["status"] == "session"
            )

            print(
                f"ПК в памяти: {len(PC_MONITOR)} | "
                f"На сессии: {sessions_count}"
            )

        except Exception as e:

            print(
                "ОШИБКА МОНИТОРА:",
                e
            )

        await asyncio.sleep(5)
