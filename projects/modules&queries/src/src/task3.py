"""Завдання 3: програма, що використовує одразу 3 модулі.

Модулі: random, datetime, requests.
Програма вибирає випадковий сайт, надсилає до нього запит
і виводить код відповіді разом із поточним часом.
"""

import random
from datetime import datetime

import requests

SITES = [
    "https://api.github.com",
    "https://www.python.org",
    "https://pypi.org",
]


def run() -> None:
    url = random.choice(SITES)                         
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  

    try:
        response = requests.get(url, timeout=5)        
        print(f"[{now}] {url} -> {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"[{now}] {url} -> помилка з'єднання: {error}")