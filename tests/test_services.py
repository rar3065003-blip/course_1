from typing import Any

from src.services import find_word


def test_find_word(data_transactions: Any) -> None:
    data = find_word(data_transactions, "Пополнение торгового счета")
    assert data[0].get("Дата операции") == "09.02.2018 16:38:24"
