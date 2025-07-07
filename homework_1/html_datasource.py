import requests
from homework_1.constants import VARIANT_URL, HEADERS, SLEEP_TIME


def get_index_html() -> str:
    response = requests.get(VARIANT_URL, headers=HEADERS)
    response.raise_for_status()
    return response.text


def get_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text
