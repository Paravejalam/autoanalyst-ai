import pandas as pd
from typing import Tuple, Dict, Any
from ml.preprocessing.cleaner import clean_data

def process_file_data(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Load data from file, clean it, and extract basic statistics.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            # For xlsx, xls files
            df = pd.read_excel(file_path)
            
        if df.empty:
            raise ValueError("The uploaded file contains no data.")
    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded CSV file is empty.")
    except Exception as e:
        raise ValueError(f"Failed to load or parse file: {str(e)}")
    
    # Run data cleaning
    df_cleaned = clean_data(df)

    rows, cols = df_cleaned.shape
    
    # Calculate missing values before replacing with "NA" (using original df is optional, here we use original data)
    missing_values = df.isnull().sum().to_dict()
    dtypes = df.dtypes.astype(str).to_dict()

    try:
        # Include all for categorical + numerical, and fill nan to simplify JSON casting
        stats = df_cleaned.describe(include='all').fillna("").to_dict()
    except Exception:
        stats = {}
        
    summary = {
        "rows": rows,
        "columns_count": cols,
        "columns": list(df.columns),
        "missing_values": missing_values,
        "data_types": dtypes,
        "stats": stats
    }
    
    return df_cleaned, summary
