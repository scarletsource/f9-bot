import os
import requests

BASE_URL = os.getenv("LANGAME_URL")
API_KEY = os.getenv("LANGAME_API_KEY")

headers = {
    "X-Api-Key": API_KEY
}

def get_busy_pcs():

    data = get_guest_sessions()

    busy = []

    for session in data["data"]:

        if session["date_stop"] is None:

            busy.append(
                session["UUID"]
            )

    return busy

def get_guest_sessions():

    response = requests.get(
        f"{BASE_URL}/guests/sessions",
        headers=headers
    )

    return response.json()

def get_busy_pcs():

    data = get_guest_sessions()

    busy = []

    for session in data["data"]:

        if session["date_stop"] is None:

            busy.append(
                session["UUID"]
            )

    return busy
    
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

    return response.json()

def get_products():

    response = requests.get(
        f"{BASE_URL}/products/list",
        headers=headers
    )

    return response.json()


def get_pc_list():

    response = requests.get(
        f"{BASE_URL}/pc/list",
        headers=headers
    )

    return {
        "status_code": response.status_code,
        "text": response.text
    }

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
