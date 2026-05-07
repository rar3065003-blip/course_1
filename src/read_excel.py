import os.path

import pandas as pd


def read_excel_file(excel_data) -> pd.DataFrame:
    """Принимает excel файл и возвращает объект pd.DataFrame"""
    file_exist = os.path.exists(excel_data)
    if file_exist:
        result_data = pd.read_excel(excel_data, engine="openpyxl")
        return result_data
    raise ValueError("Файл не существует")
