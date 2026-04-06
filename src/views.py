"ПРинимает data и time"
import os

from config import ROOT_DIR
from src.read_excel import read_excel_file
from src.utils import get_greeting, get_cards, get_top_transactions, get_currency_rates, get_stock_prices


def main_page(date_start:str):
    """YYYY-MM-DD HH:MM:SS"""
    input_df = read_excel_file(os.path.join(ROOT_DIR, "data", "operations.xlsx"))
    greeting = get_greeting()
    cards = get_cards(input_df)
    top_transactions = get_top_transactions(input_df)
    currency_rates = get_currency_rates("USD", 79.05)
    stock_prices = get_stock_prices("IBM")
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rate": currency_rates,
        "stock_prices": stock_prices
        }
    return result


"""
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}"""