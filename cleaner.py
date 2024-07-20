import pandas as pd


def clean(df):
    #  Raqamli ustunlar uchun yo'q bo'lgan qiymatlarni median bilan to'ldirish
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].median())

    # Kategoriyali ustunlar uchun yo'q bo'lgan qiymatlarni moda bilan to'ldirish
    categorical_columns = df.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        df[column] = df[column].fillna(df[column].mode()[0])
    return df

