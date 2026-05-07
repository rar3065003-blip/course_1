"ПРинимает data и time"

import json
import os
import logging
from datetime import datetime

from config import ROOT_DIR
from src.read_excel import read_excel_file
from src.reports import spending_by_category
from src.services import find_word
from src.utils import (
    get_greeting,
    get_cards,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
    data_time_range,
)
from user_settings import read_user_settings

"""
сделать логгер, 
анализ диапазона с начала месяца
тесты mock и т.п.
в отчетах реализовать декоратор для функции отчетов
"""
logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs//views.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_page(date_start: str) -> str | None:
    """Выполнение вызова готовых функций поэтапно согласно заданию"""

    try:
        logger.info("Начало выполнения функции")
        input_df = read_excel_file(os.path.join(ROOT_DIR, "data", "operations.xlsx"))
        start_of_time, end_of_time = data_time_range(date_start)
        cards = get_cards(input_df)
        word_finder = find_word(input_df, "переводы")
        spend_money = spending_by_category(
            input_df, "переводы", date="01.12.2021 00:00:00"
        )
        user_currencies, user_stocks = read_user_settings(
            os.path.join(ROOT_DIR, "user_settings.json")
        )
        greeting = get_greeting()
        top_transactions = get_top_transactions(input_df)
        currency_rates = get_currency_rates(user_currencies)
        stock_prices = get_stock_prices(user_stocks)
        result = {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rate": currency_rates,
            "stock_prices": stock_prices,
        }
        return json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as ex:
        logger.error(f"Ошибка выполнения: {ex}")
        return None
