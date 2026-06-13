import asyncio
import time
from datetime import datetime

from langame_api import (
    get_pc_linking,
    get_guest_sessions
)

PC_MONITOR = {}


def get_monitor_status(uuid):

    if uuid not in PC_MONITOR:
        return "shutdown"

    return PC_MONITOR[uuid]["status"]


def get_monitor_guest(uuid):

    if uuid not in PC_MONITOR:
        return None

    return PC_MONITOR[uuid]["guest_id"]


def get_monitor_pc_name(uuid):

    if uuid not in PC_MONITOR:
        return "Неизвестно"

    return PC_MONITOR[uuid]["pc_name"]


def get_monitor_fiscal_name(uuid):

    if uuid not in PC_MONITOR:
        return "-"

    return PC_MONITOR[uuid]["fiscal_name"]


def get_monitor_type(uuid):

    if uuid not in PC_MONITOR:
        return None

    return PC_MONITOR[uuid]["type_id"]


def get_monitor_start_time(uuid):

    if uuid not in PC_MONITOR:
        return "-"

    start_time = PC_MONITOR[uuid]["date_start"]

    if start_time is None:
        return "-"

    return start_time


def get_monitor_play_time(uuid):

    if uuid not in PC_MONITOR:
        return "-"

    start_time = PC_MONITOR[uuid]["date_start"]

    if start_time is None:
        return "-"

    try:

        start = datetime.strptime(
            start_time,
            "%Y-%m-%d %H:%M:%S"
        )

        delta = datetime.now() - start

        hours = delta.seconds // 3600

        minutes = (delta.seconds % 3600) // 60

        return f"{hours}ч {minutes}м"

    except:

        return "-"


async def monitor_pcs():

    while True:

        try:

            data = get_pc_linking()

            sessions_data = get_guest_sessions()

            # Сбрасываем все статусы
            for uuid in PC_MONITOR:

                PC_MONITOR[uuid]["status"] = "free"

                PC_MONITOR[uuid]["guest_id"] = None

                PC_MONITOR[uuid]["date_start"] = None

            # Обновляем список ПК
            for pc in data["data"]:

                uuid = pc["UUID"]

                if uuid not in PC_MONITOR:

                    PC_MONITOR[uuid] = {

                        "pc_name": pc["name"],

                        "fiscal_name": pc["fiscal_name"],

                        "type_id": pc["packets_type_PC"],

                        "guest_id": None,

                        "date_start": None,

                        "status": "free",

                        "last_seen": time.time()
                    }

                else:

                    PC_MONITOR[uuid]["pc_name"] = pc["name"]

                    PC_MONITOR[uuid]["fiscal_name"] = pc["fiscal_name"]

                    PC_MONITOR[uuid]["type_id"] = pc["packets_type_PC"]

                    PC_MONITOR[uuid]["last_seen"] = time.time()

            # Отмечаем активные сессии
            if sessions_data["status"]:

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
