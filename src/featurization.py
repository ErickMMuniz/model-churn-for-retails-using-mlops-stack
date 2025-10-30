import pandas as pd
import dvc.api
from utils import log_function_call


params = dvc.api.params_show()


@log_function_call
def fetch_data() -> pd.DataFrame:
    path = params["paths"]["prepared_data"]
    df = pd.read_csv(path, encoding="utf-8")
    return df


def process() -> None:
    df = fetch_data()
    return df


if __name__ == "__main__":
    a = process()
    print(a)
