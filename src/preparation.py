import pandas as pd
import dvc.api
from utils import log_function_call
from etl.extract import (
    check_existing_columns,
    drop_empty_invoice_id,
    drop_unit_price_less_than_zero,
    extract_data,
    filter_invoices_with_non_negative_quantity,
    filter_shop_tiems_with_empty_description_and_zero_unit_price,
)
from etl.transform import change_columns_types, sample_dataframe

params = dvc.api.params_show()


@log_function_call
def fetch_data() -> pd.DataFrame:
    path_data = params["paths"]["data"]
    df = extract_data(path_data)
    return df


@log_function_call
def sample_data(df: pd.DataFrame) -> pd.DataFrame:
    sample_size = params["preparation"]["sample_size"]
    random_state = params["variables"]["random_state"]
    df = sample_dataframe(df, sample_size, random_state)
    return df


@log_function_call
def solve_null_data(df: pd.DataFrame) -> pd.DataFrame:
    df = drop_empty_invoice_id(df)
    return df.dropna()


@log_function_call
def assert_columns(df: pd.DataFrame) -> None:
    columns: list[str] = params["preparation"]["columns"]
    df = check_existing_columns(df, columns)
    return df


@log_function_call
def check_columns_types(df: pd.DataFrame) -> pd.DataFrame:
    return change_columns_types(df, params["preparation"]["types"]["columns"])


@log_function_call
def check_model_constriants(df: pd.DataFrame) -> pd.DataFrame:
    df = filter_shop_tiems_with_empty_description_and_zero_unit_price(df)
    df = filter_invoices_with_non_negative_quantity(df)
    df = drop_unit_price_less_than_zero(df)
    return df


def process() -> None:
    df_raw = fetch_data()
    df = assert_columns(df_raw)
    df = solve_null_data(df)
    df = check_model_constriants(df)
    df = check_columns_types(df)
    df = sample_data(df)

    path_prepared_data = params["paths"]["prepared_data"]
    df.to_csv(path_prepared_data, index=False, encoding="utf-8")

    print(
        f"Raw data has {df_raw.shape[0]} rows, prepared data has {df.shape[0]} rows. Difference: {df_raw.shape[0] - df.shape[0]}"
    )


if __name__ == "__main__":
    process()
