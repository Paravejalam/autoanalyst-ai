import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic data cleaning on the input dataframe.
    """
    # Create a copy to avoid SettingWithCopyWarning
    df_cleaned = df.copy()

    # Handle missing values
    df_cleaned = df_cleaned.fillna("NA")

    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()

    return df_cleaned
