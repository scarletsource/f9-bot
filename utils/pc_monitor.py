import asyncio
import time
from datetime import datetime

from langame_api import (
    get_pc_linking,
    get_pc_types,
    get_guest_sessions
)

PC_MONITOR = {}


def get_pc_by_uuid(uuid):

    return PC_MONITOR.get(uuid)


def get_all_pcs():

    return PC_MONITOR


def get_all_zones():

    zones = {}

    for pc in PC_MONITOR.values():

        if pc["type_id"] not in zones:

            zones[pc["type_id"]] = pc["zone_name"]

    return zones


def get_monitor_pc_name(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "Неизвестно"

    return pc["pc_name"]


def get_monitor_zone_name(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "Неизвестно"

    return pc["zone_name"]


def get_monitor_guest(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return None

    return pc["guest_id"]


def get_monitor_play_time(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "-"

    start_time = pc["date_start"]

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


#
# Состояние питания
#

def set_power_state(uuid, state):

    if uuid in PC_MONITOR:

        PC_MONITOR[uuid]["power_state"] = state


def get_power_state(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "offline"

    return pc["power_state"]


#
# Режим
#

def set_mode_state(uuid, state):

    if uuid in PC_MONITOR:

        PC_MONITOR[uuid]["mode_state"] = state


def get_mode_state(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "normal"

    return pc["mode_state"]


#
# Действие
#

def set_action_state(uuid, state):

    if uuid in PC_MONITOR:

        PC_MONITOR[uuid]["action_state"] = state


def get_action_state(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "none"

    return pc["action_state"]


async def monitor_pcs():

    while True:

        try:

            data = get_pc_linking()

            types_data = get_pc_types()["data"]

            sessions_data = get_guest_sessions()

            #
            # Сбрасываем игровые сессии
            #

            for uuid in PC_MONITOR:

                PC_MONITOR[uuid]["session_state"] = False

                PC_MONITOR[uuid]["guest_id"] = None

                PC_MONITOR[uuid]["date_start"] = None

            #
            # Обновляем список ПК
            #

            for pc in data["data"]:

                uuid = pc["UUID"]

                zone_name = "Неизвестно"

                for zone in types_data:

                    if zone["id"] == pc["packets_type_PC"]:

                        zone_name = zone["name"]

                        break

                if uuid not in PC_MONITOR:

                    PC_MONITOR[uuid] = {

                        "pc_name": pc["name"],

                        "fiscal_name": pc["fiscal_name"],

                        "type_id": pc["packets_type_PC"],

                        "zone_name": zone_name,

                        #
                        # Игровая сессия
                        #

                        "session_state": False,

                        "guest_id": None,

                        "date_start": None,

                        #
                        # Питание
                        #

                        "power_state": "online",

                        #
                        # Режим
                        #

                        "mode_state": "normal",

                        #
                        # Текущее действие
                        #

                        "action_state": "none",

                        "last_seen": time.time()

                    }

                else:

                    PC_MONITOR[uuid]["pc_name"] = pc["name"]

                    PC_MONITOR[uuid]["fiscal_name"] = pc["fiscal_name"]

                    PC_MONITOR[uuid]["type_id"] = pc["packets_type_PC"]

                    PC_MONITOR[uuid]["zone_name"] = zone_name

                    PC_MONITOR[uuid]["last_seen"] = time.time()

            #
            # Активные игровые сессии
            #

            if sessions_data["status"]:

                for session in sessions_data["data"]:

                    if session["date_stop"] is not None:

                        continue

                    uuid = session["UUID"]

                    if uuid not in PC_MONITOR:

                        continue

                    PC_MONITOR[uuid]["session_state"] = True

                    PC_MONITOR[uuid]["guest_id"] = session["guest_id"]

                    PC_MONITOR[uuid]["date_start"] = session["date_start"]

            sessions_count = sum(

                1

                for pc in PC_MONITOR.values()

                if pc["session_state"]

            )

            print(

                f"ПК в памяти: {len(PC_MONITOR)} | "
                f"Игровых сессий: {sessions_count}"

            )

        except Exception as e:

            print(

                "ОШИБКА МОНИТОРА:",

                e

            )

        await asyncio.sleep(5)
