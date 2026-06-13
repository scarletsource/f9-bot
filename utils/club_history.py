import json
import os
from datetime import datetime

FILE_NAME = "club_history.json"


def load_history():

    if not os.path.exists(FILE_NAME):

        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump([], f)

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


def add_club_history(text):

    history = load_history()

    time = datetime.now().strftime(
        "%H:%M"
    )

    history.insert(
        0,
        f"{time} {text}"
    )

    history = history[:20]

    save_history(history)


def get_club_history():

    return load_history()
