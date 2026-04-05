import os
from datetime import datetime
from json import JSONDecodeError

import pandas as pd
import requests
from requests import Response
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")



def get_greeting():
    day_time = datetime.now()
    hour = day_time.hour
    if 4 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards(df: pd.DataFrame) -> list[dict]:
    data_temp = df.groupby("Номер карты").agg({"Сумма операции с округлением": "sum"})
    result_cards = []
    for card_num, row in data_temp.iterrows():
        sum_operation = float(row["Сумма операции с округлением"])
        result_cards.append({
            "last_digits": card_num[-4:],
            "total_spent": sum_operation,
            "cashback": round(sum_operation / 100, 2)
        })
    return result_cards


def get_top_transactions(df: pd.DataFrame) -> list[dict]:
    data_sorted = df.sort_values(by="Сумма операции с округлением", ascending=False).head()
    result_sort = []
    for data, row in data_sorted.iterrows():
        result_sort.append({
            "date": row["Дата платежа"],
            "amount": row["Сумма операции с округлением"],
            "category": row["Категория"],
            "description": row["Описание"]
        })
    return result_sort


def exchange_rates_data(currency: str, amount: float) -> float:
    """Функция конвертации валюты по API в рубли по текущему курсу"""
    url: str = "https://api.apilayer.com/exchangerates_data/convert"
    payload: dict = {"amount": amount, "from": currency, "to": "RUB"}
    headers: dict = {"apikey": API_KEY}
    response: Response = requests.get(url, headers=headers, params=payload)

    status_code: int = response.status_code
    if status_code == 200:
        try:
            result: dict = response.json()
            result_exch: float = result.get("result", 0)
            return result_exch
        except JSONDecodeError:
            return 0
    return 0