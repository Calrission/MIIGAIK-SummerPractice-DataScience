import os.path

from homeworks.homework_1.constants import MOCK_DIR


def mock(filename: str) -> str:
    with open(os.path.join(MOCK_DIR, filename), 'r', encoding="utf-8") as f:
        return f.read()


def read(path: str) -> str:
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def url2name(url: str) -> str:
    return url.split('/')[-1]
