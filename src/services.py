import pandas as pd

"""Функция сервиса «Выгодные категории повышенного кешбэка» расположена в модуле 
services.py"""
def find_word(input_df:pd.DataFrame, word:str)->list[dict]:
    """Функция принимает категорию и возвращает список содержащий товар с наибольшим кэшбеком"""
    filtered_data = input_df[(input_df["Категория"].str.contains(word, case=False))|(input_df["Описание"].str.contains(word,case=False))]
    return filtered_data.to_dict(orient="records")