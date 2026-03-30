import pandas as pd

def process_data(file_path):
    df = pd.read_csv(file_path)

    summary = {
        "columns": list(df.columns),
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict()
    }

    return summary