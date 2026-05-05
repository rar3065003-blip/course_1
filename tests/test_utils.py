from datetime import datetime
from json import JSONDecodeError
from unittest.mock import patch

import pandas
from numpy import nan
from requests import Timeout, RequestException

from src.services import find_word
from src.utils import get_greeting, get_cards, get_top_transactions, get_currency_rates, get_stock_prices, \
    data_time_range


def test_get_greeting() -> None:
    date_morning = datetime(day=1, month=11, year=1998, hour=5, minute=0, second=0)
    date_day = datetime(day=1, month=11, year=1998, hour=12, minute=0, second=0)
    date_evening = datetime(day=1, month=11, year=1998, hour=19, minute=0, second=0)
    date_night = datetime(day=1, month=11, year=1998, hour=3, minute=0, second=0)
    with patch('datetime.datetime') as mock:
        mock.now.return_value = date_morning
        assert get_greeting() == 'Доброе утро'
        mock.now.return_value = date_day
        assert get_greeting() == 'Добрый день'
        mock.now.return_value = date_evening
        assert get_greeting() == 'Добрый вечер'
        mock.now.return_value = date_night
        assert get_greeting() == 'Доброй ночи'


def test_get_cards(data_transactions: pandas.DataFrame) -> None:
    assert get_cards(data_transactions) == [{'last_digits': '4556', 'total_spent': 80085.21, 'cashback': 800.85},
                                            {'last_digits': '5441', 'total_spent': 293347.78, 'cashback': 2933.48},
                                            {'last_digits': '7197', 'total_spent': 71832.88, 'cashback': 718.33}]


def test_get_top_transactions(data_transactions: pandas.DataFrame) -> None:
    assert get_top_transactions(data_transactions) == [{'amount': 115909.42,
                                                        'category': 'Переводы',
                                                        'date': '24.01.2018',
                                                        'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
                                                       {'amount': 115909.42,
                                                        'category': 'Переводы',
                                                        'date': '24.01.2018',
                                                        'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
                                                       {'amount': 93071.89,
                                                        'category': nan,
                                                        'date': '09.02.2018',
                                                        'description': 'Перевод с карты'},
                                                       {'amount': 87068.0,
                                                        'category': nan,
                                                        'date': '10.01.2018',
                                                        'description': 'Перевод с карты'},
                                                       {'amount': 40457.01,
                                                        'category': 'Переводы',
                                                        'date': '09.02.2018',
                                                        'description': 'Пополнение торгового счета'}]


### Проверить на 400
###linter
### docstring
# side effect
# decorators смотри страрую домашку


def test_get_currency_rates() -> None:
    with patch("requests.get") as mock_data:
        response = mock_data.return_value
        response.status_code = 200
        response.json.return_value = {"rates": {"1": 50.128}}
        assert get_currency_rates([]) == [{'currency': '1', 'rate': 50.13}]
        response.status_code = 400
        assert get_currency_rates([]) == []
        response.status_code = 200
        response.json.side_effect = JSONDecodeError("Error", " ", 67)
        assert get_currency_rates([]) == []


def test_get_stock_prices() -> None:
    with patch("requests.get") as mock_data:
        response = mock_data.return_value
        response.status_code = 200
        response.json.return_value = {"Error Message": {"1": 50.128}}
        assert get_stock_prices(['Temp']) is None
        response.json.return_value = {"Note": "Thank you for using Alpha Vantage"}
        assert get_stock_prices(['Temp']) is None
        response.json.return_value = {"123": {}}
        assert get_stock_prices(['Temp']) is None
        response.json.return_value = {"Global Quote": {"05. price": 50.128}}
        assert get_stock_prices(['Temp']) == [{"stock": "Temp", "price": 50.13}]
        response.status_code = 400
        assert get_stock_prices(['Temp']) is None
    with patch("requests.get", side_effect=JSONDecodeError("Error", " ", 67)) as mock_data:
        assert get_stock_prices(['Temp']) is None
    with patch("requests.get", side_effect=Timeout):
        assert get_stock_prices(['Temp']) is None
    with patch("requests.get", side_effect=RequestException):
        assert get_stock_prices(['Temp']) is None
    with patch("requests.get", side_effect=Exception):
        assert get_stock_prices(['Temp']) is None


def test_data_time_range() -> None:
    end_of_time = datetime(day=12, month=4, year=2026)
    start_of_time = datetime(day=1, month=4, year=2026)
    assert data_time_range("2026-04-12 00:00:00") == (start_of_time, end_of_time)

