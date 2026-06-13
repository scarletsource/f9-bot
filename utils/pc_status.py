from datetime import datetime

from langame_api import get_pc_session


def get_pc_user(uuid):

    session = get_pc_session(uuid)

    if session is None:

        return "Свободен"

    return f"ID {session['guest_id']}"


def get_pc_start_time(uuid):

    session = get_pc_session(uuid)

    if session is None:

        return "-"

    return session["date_start"]


def get_pc_play_time(uuid):

    session = get_pc_session(uuid)

    if session is None:

        return "-"

    start = datetime.strptime(
        session["date_start"],
        "%Y-%m-%d %H:%M:%S"
    )

    delta = datetime.now() - start

    hours = delta.seconds // 3600

    minutes = (delta.seconds % 3600) // 60

    return f"{hours}ч {minutes}м"
