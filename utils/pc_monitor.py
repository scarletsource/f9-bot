import time

PC_MONITOR = {}


def update_pc(uuid, status):

    PC_MONITOR[uuid] = {
        "status": status,
        "last_seen": time.time()
    }


def get_pc_status(uuid):

    if uuid not in PC_MONITOR:

        return "shutdown"

    return PC_MONITOR[uuid]["status"]
