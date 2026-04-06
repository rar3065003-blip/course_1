import os
from datetime import datetime
from json import JSONDecodeError
import pandas as pd
import requests
from requests import Response, Timeout, RequestException
from dotenv import load_dotenv
load_dotenv()
API_KEY_1 = os.getenv("API_KEY_LAYER")
API_KEY_2 = os.getenv("API_KEY_ALPHAVANTAGE")



def get_greeting():
    """Приветствует пользователя в зависимости от времени суток"""
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
    """Возвращает номер карты и сумму операции с кэшбеком и округлением"""
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


def get_currency_rates(currency: str, rate: float) -> float:
    """Функция конвертации валюты по API в рубли по текущему курсу"""
    url: str = "https://api.apilayer.com/exchangerates_data/convert"
    payload: dict = {"amount": rate, "from": currency, "to": "RUB"}
    headers: dict = {"apikey": API_KEY_1}
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


def get_stock_prices(
    stock: str,
    interval: str = "5min",
    api_key: str = API_KEY_2
) -> float | None:

    url = 'https://www.alphavantage.co/query'
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": stock,
        "interval": interval,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "Error Message" in data:
                print(f"Ошибка API: {data['Error Message']}")
                return None

            if "Note" in data and "Thank you for using Alpha Vantage" in data["Note"]:
                print("Ошибка: достигнут лимит запросов к API (5/мин)")
                return None

            global_quote = data.get("Global Quote", {})
            if not global_quote:
                print("Ошибка: поле 'Global Quote' отсутствует в ответе API")
                return None

            # Извлекаем все необходимые цены
            open_price = global_quote.get("02. open")
            high_price = global_quote.get("03. high")
            low_price = global_quote.get("04. low")
            current_price = global_quote.get("05. price")

            # Проверяем, что все цены присутствуют
            if not all([open_price, high_price, low_price, current_price]):
                print(f"Данные: {global_quote}")
                return None

            open_float = float(open_price)
            high_float = float(high_price)
            low_float = float(low_price)
            current_float = float(current_price)

            average_price = round((open_float + high_float + low_float + current_float) / 4, 2)
            return average_price

        else:
            print(f"Ошибка HTTP: статус {response.status_code}")
            return None
    except JSONDecodeError:
        print("Ошибка: не удалось распарсить JSON. Ответ сервера:")
        print(response.text)
        return None
    except Timeout:
        print("Ошибка: запрос превысил таймаут (10 секунд)")
        return None
    except RequestException as e:
        print(f"Сетевая ошибка: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None