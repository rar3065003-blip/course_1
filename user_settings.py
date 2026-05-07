import json
import os.path


def read_user_settings(path: str) -> tuple[list, list]:
    """Принимает json файл и возвращает python строки"""
    temp = os.path.exists(path)
    if temp:
        with open(path, "r", encoding="utf-8") as file:
            json_settings = json.load(file)
            user_currencies = json_settings.get("user_currencies", [])
            user_stocks = json_settings.get("user_stocks", [])
        return user_currencies, user_stocks
    return [], []
