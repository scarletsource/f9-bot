import os
import time
import requests

BASE_URL = os.getenv("LANGAME_URL")
API_KEY = os.getenv("LANGAME_API_KEY")

headers = {
    "X-Api-Key": API_KEY
}

# Кэш активных сессий
SESSIONS_CACHE = []
LAST_UPDATE = 0


def get_guest_sessions():

    response = requests.get(
        f"{BASE_URL}/guests/sessions",
        headers=headers
    )

    return response.json()


def get_cached_sessions():

    global SESSIONS_CACHE
    global LAST_UPDATE

    now = time.time()

    # Обновляем кэш раз в 5 секунд
    if now - LAST_UPDATE > 5:

        response = requests.get(
            f"{BASE_URL}/guests/sessions",
            headers=headers
        )

        data = response.json()

        if data["status"]:

            SESSIONS_CACHE = data["data"]

            LAST_UPDATE = now

    return SESSIONS_CACHE


def get_busy_pcs():

    sessions = get_cached_sessions()

    busy = []

    for session in sessions:

        if session["date_stop"] is None:

            busy.append(
                session["UUID"]
            )

    return busy


def get_pc_session(uuid):

    sessions = get_cached_sessions()

    for session in sessions:

        if (
            session["UUID"] == uuid
            and session["date_stop"] is None
        ):

            return session

    return None


def get_clubs():

    response = requests.get(
        f"{BASE_URL}/clubs/list",
        headers=headers
    )

    return response.json()


def get_routes():

    response = requests.get(
        f"{BASE_URL}/routes",
        params={
            "api_key": API_KEY
        }
    )

    return {
        "status_code": response.status_code,
        "text": response.text
    }


def get_products():

    response = requests.get(
        f"{BASE_URL}/products/list",
        headers=headers
    )

    return response.json()


def pc_manage(command, uuid):

    payload = {
        "club_id": 1,
        "command": command,
        "uuids": [uuid]
    }

    response = requests.post(
        f"{BASE_URL}/pc/manage",
        headers=headers,
        json=payload
    )

    return response.json()


def get_pc_types():

    response = requests.get(
        f"{BASE_URL}/global/types_of_pc_in_clubs/list",
        headers=headers
    )

    return {
        "status_code": response.status_code,
        "text": response.text
    }


def get_pc_linking():

    response = requests.get(
        f"{BASE_URL}/global/linking_pc_by_type/list",
        headers=headers
    )

    return response.json()


def get_adminconsole():

    response = requests.get(
        f"{BASE_URL}/ver/get_adminconsole",
        headers=headers
    )

    return response.json()
