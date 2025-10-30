from pandas import DataFrame
import pandas as pd

def change_columns_types(df: pd.DataFrame, types: dict[str, str]) -> pd.DataFrame:
    """
    Changes the data types of specified columns in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        types (dict[str, str]): A dictionary where keys are column names and values are
                                 the desired data type names as strings (e.g., 'int', 'float').

    Returns:
        pd.DataFrame: The DataFrame with updated column types.
    """
    columns_types = {k: from_str_to_type(v) for k, v in types.items()}
    return df.astype(columns_types)

def sample_dataframe(df: pd.DataFrame, sample_size: float, random_state: int) -> pd.DataFrame:
    """
    Samples a DataFrame based on a specified sample size.

    Args:
        df (pd.DataFrame): The input DataFrame.
        sample_size (float): The proportion of the DataFrame to sample (e.g., 0.1 for 10%).
                             If 1, the original DataFrame is returned.
        random_state (int): Seed for random number generator for reproducibility.

    Returns:
        pd.DataFrame: The sampled DataFrame.
    """
    n = int(df.shape[0] * sample_size)
    if sample_size == 1:
        return df
    else:
        return df.sample(n=n, random_state=random_state)

def from_str_to_type(type_name: str):
    """
    Converts a string representation of a type to its actual type.

    Args:
        type_name (str): The name of the type as a string (e.g., 'int', 'float').

    Returns:
        type: The actual Python type or a string for pandas datetime.
    
    Note: This function is primarily designed for use with `pd.Series` types.
    """
    match type_name:
        case 'int':
            return int
        case 'float':
            return float
        case 'str':
            return str
        case 'bool':
            return bool
        case 'datetime':
            return 'datetime64[ns]'
        case _:
            return 'object'