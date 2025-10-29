import pandas as pd
import dvc.api
from utils import log_function_call, from_str_to_type

params = dvc.api.params_show()

@log_function_call
def fetch_data()-> pd.DataFrame:
    path_data = params['paths']['data']
    try:
        df = pd.read_csv(path_data, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(path_data, encoding='ISO-8859-1')
    return df

@log_function_call
def sample_data(df: pd.DataFrame) -> pd.DataFrame:
    sample_size = params['preparation']['sample_size']
    n = int(df.shape[0] * sample_size)
    if sample_size == 1:
        return df
    else:
        return df.sample(n=n)

@log_function_call 
def solve_null_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()

@log_function_call
def assert_columns(df: pd.DataFrame) -> None:
    columns: list[str] = params['preparation']['columns']
    for c in columns:
        assert c in df.columns, "Missing column: {}".format(c)
    return df

@log_function_call
def check_columns_types(df: pd.DataFrame) -> pd.DataFrame:
    columns_types: dict[str, str] = params['preparation']['types']['columns']
    columns_types = {k: from_str_to_type(v) for k, v in columns_types.items()}
    return df.astype(columns_types)

@log_function_call
def check_model_constriants(df: pd.DataFrame) -> pd.DataFrame:
    #TODO: After featurization
    return df


def process() -> None:
    df = fetch_data()
    df = assert_columns(df)
    df = solve_null_data(df)
    df = check_columns_types(df)
    df = check_model_constriants(df)
    df = sample_data(df)

    path_prepared_data = params['paths']['prepared_data']
    df.to_csv(path_prepared_data, index=False, encoding='utf-8')


if __name__ == "__main__":
    process()
    