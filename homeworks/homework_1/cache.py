import os.path
from homeworks.homework_1.constants import SAVE_DIR


def prepare():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def check_is_saved(name: str) -> bool:
    return os.path.exists(os.path.join(SAVE_DIR, name))


def save(name: str, html: str):
    with open(os.path.join(SAVE_DIR, name), 'w', encoding="utf-8") as file:
        file.write(html)


def read(name: str) -> str:
    with open(os.path.join(SAVE_DIR, name), 'r', encoding="utf-8") as file:
        return file.read()
