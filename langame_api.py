import os
import requests

BASE_URL = os.getenv("LANGAME_URL")
API_KEY = os.getenv("LANGAME_API_KEY")

headers = {
    "X-Api-Key": API_KEY
}


def get_clubs():

    response = requests.get(
        f"{BASE_URL}/clubs/list",
        headers=headers
    )

    return response.json()


def get_routes():

    response = requests.get(
        f"{BASE_URL}/routes",
        headers=headers
    )

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

    return response.json()
