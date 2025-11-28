
import pandas as pd

def handle_missing_values(df):
    """Fills missing numeric values with the mean and categorical values with the mode."""
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)
    return df

def handle_outliers(df):
    """Handles outliers using the IQR method."""
    for col in df.select_dtypes(include=['number']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

def preprocess_data(df):
    df = handle_missing_values(df)
    # df = handle_outliers(df)
    return df
