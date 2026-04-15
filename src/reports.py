import functools
import logging
from collections.abc import Callable
from datetime import datetime, time
from typing import Optional, Any
import pandas as pd
from pandas import DateOffset
from config import ROOT_DIR

logger = logging.getLogger('reports')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{ROOT_DIR}/logs/reports.log", encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def log(filename: Optional[str] = "default.log") -> Callable:
    """Функция записи лога выполнения исполняемой функции -
    сохраняет в лог в файл при задании имени или выводит в консоль"""
    def decorator(func: Callable) -> Callable:
        """Принимает вызов функции"""
        @functools.wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            """Оборачиваем функцию и запускаем запись и вычисление времени работы"""
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as w:
                result = f"{func.__name__} raised with arguments {args, kwargs}\n but it didn`t worked, error:{str(w)} \n"
                logger.info (result)
            finally:
                logger.info(result)
                with open(f"{ROOT_DIR}/data/{filename}", mode="a", encoding="utf-8") as x:
                    x.write(result + "\n")
            return result
        return wrapper
    return decorator

@log()
def spending_by_category(transactions: pd.DataFrame,category:str,
                        date: Optional[str] = None) -> pd.DataFrame:
    """Принимает DataFrame, возвращает операции за последние 3 месяца в строковом виде"""
    if date is None:
        end_of_time = datetime.now()
    else:
        end_of_time = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    start_time = end_of_time-DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    filter_transaction = transactions[
        (transactions["Дата операции"]>= start_time)&
        (transactions["Дата операции"]<= end_of_time)&
        (transactions["Категория"].str.contains(category, case=False))
    ]
    return filter_transaction

