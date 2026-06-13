from langame_api import (
    get_guest_sessions
)


def get_real_session_by_pc(uuid):

    sessions = get_guest_sessions()

    if not sessions["status"]:

        return None

    for session in sessions["data"]:

        if (
            session["UUID"] == uuid
            and session["date_stop"] is None
        ):

            return session

    return None


def get_real_status(uuid):

    session = get_real_session_by_pc(uuid)

    if session is None:

        return "free"

    return "session"


def get_real_user(uuid):

    session = get_real_session_by_pc(uuid)

    if session is None:

        return "Свободен"

    return f"ID {session['guest_id']}"
