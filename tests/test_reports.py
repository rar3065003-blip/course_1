from typing import Any

from pandas import Timestamp

from config import ROOT_DIR
from src.reports import log, spending_by_category


def test_log() -> None:
    filename = "default.log"
    log()(lambda x, y: x / y)(4, 2)
    with open(f"{ROOT_DIR}/data/{filename}", mode="r", encoding="utf-8") as f:
        last_line = f.readlines()[-1]
        assert last_line == "2.0\n"


def test_log_exception() -> None:
    filename = "default.log"
    log()(lambda x, y: x / y)(4, 0)
    with open(f"{ROOT_DIR}/data/{filename}", mode="r", encoding="utf-8") as f:
        last_line = f.readlines()[-1]
        assert last_line == (
            "<lambda> raised with arguments ((4, 0), {}) but it didn`t worked, " "error:division by zero\n"
        )


def test_spending_by_category(data_transactions: Any) -> None:
    data = spending_by_category(data_transactions, "Переводы")
    data_dict = data.to_dict(orient="records")
    assert data_dict == []
    data2 = spending_by_category(data_transactions, "Переводы", date="02.03.2018 00:00:00")
    assert data2.to_dict(orient="records")[1].get("Дата операции") == Timestamp("2018-01-23 21:39:01")
