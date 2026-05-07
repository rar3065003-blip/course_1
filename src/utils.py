import datetime
import logging
import os
from json import JSONDecodeError
import pandas as pd
import requests
from requests import Response, Timeout, RequestException
from dotenv import load_dotenv

from config import ROOT_DIR

load_dotenv()
API_KEY_1 = os.getenv("API_KEY_LAYER")
API_KEY_2 = os.getenv("API_KEY_ALPHAVANTAGE")

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greeting() -> str:
    """Приветствует пользователя в зависимости от времени суток"""

    logger.info("Начало выполнения функции")

    day_time = datetime.datetime.now()
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
    """Возвращает номер карты и сумму операции с кэшбеком и округлением"""
    logger.info("Начало выполнения функции")

    data_temp = df.groupby("Номер карты").agg({"Сумма операции с округлением": "sum"})
    result_cards = []
    for card_num, row in data_temp.iterrows():
        assert isinstance(card_num, str)
        sum_operation = float(row["Сумма операции с округлением"].item())
        result_cards.append(
            {
                "last_digits": card_num[-4:],
                "total_spent": sum_operation,
                "cashback": round(sum_operation / 100, 2),
            }
        )
    return result_cards


def get_top_transactions(df: pd.DataFrame) -> list[dict]:
    """Принимает таблицу, возвращает транзакцию с указанием категорий и описанием"""
    logger.info("Начало выполнения функции")

    data_sorted = df.sort_values(
        by="Сумма операции с округлением", ascending=False
    ).head()
    result_sort = []
    for data, row in data_sorted.iterrows():
        result_sort.append(
            {
                "date": row["Дата платежа"],
                "amount": row["Сумма операции с округлением"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    return result_sort


def get_currency_rates(currency: list) -> list:
    """Функция возвращает курс валюты по API"""
    currency_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
    url: str = f"https://api.apilayer.com/exchangerates_data/{currency_date}"
    payload: dict = {"base": "RUB", "symbols": ",".join(currency)}
    headers: dict = {"apikey": API_KEY_1}
    response: Response = requests.get(url, headers=headers, params=payload)
    temp = []
    status_code: int = response.status_code
    if status_code == 200:
        try:
            logger.info(f"Ответ API получен")
            result: dict = response.json()
            result_exch: dict = result.get("rates", {})
            for k, v in result_exch.items():
                temp.append({"currency": k, "rate": round(v, 2)})
            return temp
        except JSONDecodeError as ex:
            logger.info(f"Произошла ошибка:{ex}")  # дополнить ошибки
            return []
    return []


def get_stock_prices(stocks: list, api_key: str = API_KEY_2) -> list| str| None:
    """Возвращает стоимость запрошенных тикетов акций в рублях"""
    url = "https://www.alphavantage.co/query"
    stock_list = []
    for stock in stocks:
        params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": api_key}

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                logger.info(f"Ответ API получен")
                data: dict = response.json()

                if "Error Message" in data:
                    print(f"Ошибка API: {data['Error Message']}")
                    logger.info(f"Ошибка API: {data['Error Message']}")
                    return None

                if (
                    "Note" in data
                    and "Thank you for using Alpha Vantage" in data["Note"]
                ):
                    print("Ошибка: достигнут лимит запросов к API (5/мин)")
                    logger.info("Ошибка: достигнут лимит запросов к API (5/мин)")
                    return None
                global_quote = data.get("Global Quote", {})
                if not global_quote:
                    print("Ошибка: поле 'Global Quote' отсутствует в ответе API")
                    return None

                logger.info("Извлекаем все необходимые цены")
                current_price = global_quote.get("05. price")
                current_float = float(current_price)

                average_price = round(current_float, 2)
                stock_list.append({"stock": stock, "price": average_price})

            else:
                print(f"Ошибка HTTP: статус {response.status_code}")
                logger.info(f"Ошибка HTTP: статус {response.status_code}")
                return None
        except JSONDecodeError as ex:
            logger.info("Ошибка: не удалось распарсить JSON. Ответ сервера:")
            print("Ошибка: не удалось распарсить JSON. Ответ сервера:")
            return None
        except Timeout:
            print("Ошибка: запрос превысил таймаут (10 секунд)")
            return None
        except RequestException as e:
            print(f"Сетевая ошибка: {e}")
            logger.info(f"Сетевая ошибка: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            logger.info(f"Неожиданная ошибка: {e}")
            return None
    return stock_list


def data_time_range(date_start_range: str) -> tuple[datetime.datetime, datetime.datetime]:
    """Возвращает временной период транзакций"""
    end_of_time = datetime.datetime.strptime(date_start_range, "%Y-%m-%d %H:%M:%S")
    start_of_time = datetime.datetime(
        day=1, month=end_of_time.month, year=end_of_time.year
    )
    return start_of_time, end_of_time
