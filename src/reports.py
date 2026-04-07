from datetime import datetime
from typing import Optional

import pandas as pd
from pandas import DateOffset


def spending_by_category(transactions: pd.DataFrame,category:str,
                        date: Optional[str] = None) -> pd.DataFrame:
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

