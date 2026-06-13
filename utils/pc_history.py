import json
import os
from datetime import datetime

FILE_NAME = "pc_history.json"


def load_history():

    if not os.path.exists(FILE_NAME):

        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history):

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(
            history,
            f,
            ensure_ascii=False,
            indent=4
        )


def add_history(uuid, action):

    history = load_history()

    if uuid not in history:

        history[uuid] = []

    time = datetime.now().strftime(
        "%H:%M"
    )

    history[uuid].insert(
        0,
        f"{time} {action}"
    )

    history[uuid] = history[uuid][:5]

    save_history(history)


def get_history(uuid):

    history = load_history()

    return history.get(
        uuid,
        []
    )
