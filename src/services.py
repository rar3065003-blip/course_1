import pandas as pd
def find_word(input_df:pd.DataFrame, word:str)->list[dict]:
    filtered_data = input_df[(input_df["Категория"].str.contains(word, case=False))|(input_df["Описание"].str.contains(word,case=False))]
    return filtered_data.to_dict(orient="records")