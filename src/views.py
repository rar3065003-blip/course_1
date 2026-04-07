"ПРинимает data и time"
import os

from config import ROOT_DIR
from src.read_excel import read_excel_file
from src.reports import spending_by_category
from src.services import find_word
from src.utils import get_greeting, get_cards, get_top_transactions, get_currency_rates, get_stock_prices
from user_settings import read_user_settings
"""
сделать логгер, 
анализ диапазона с начала месяца
тесты mock и т.п.
в отчетах реализовать декоратор для функции отчетов
"""

def main_page(date_start:str):
    """YYYY-MM-DD HH:MM:SS"""
    input_df = read_excel_file(os.path.join(ROOT_DIR, "data", "operations.xlsx"))
    # word_finder = find_word(input_df, "переводы")
    spend_money = spending_by_category(input_df, "переводы",  date = "01.12.2021 00:00:00")
    print(spend_money)
    # user_currencies, user_stocks = read_user_settings(os.path.join(ROOT_DIR, "user_settings.json"))
    # print(user_currencies, user_stocks)
    # greeting = get_greeting()
    # cards = get_cards(input_df)
    # top_transactions = get_top_transactions(input_df)
    # currency_rates = get_currency_rates(user_currencies)
    # stock_prices = get_stock_prices(user_stocks)
    # result = {
    #     "greeting": greeting,
    #     "cards": cards,
    #     "top_transactions": top_transactions,
    #     "currency_rate": currency_rates,
    #     "stock_prices": stock_prices
    #     }
    # return result
