import pandas as pd
import dvc.api
from etl.transform import change_columns_types
from utils import log_function_call
from etl.extract import extract_data


params = dvc.api.params_show()


@log_function_call
def fetch_data() -> pd.DataFrame:
    path = params["paths"]["prepared_data"]
    df = extract_data(path)
    return df

def set_columns_types(df: pd.DataFrame) -> pd.DataFrame:
    return change_columns_types(df, params["preparation"]["types"]["columns"])

@log_function_call
def make_featurization(df: pd.DataFrame) -> pd.DataFrame:
    customers = df['CustomerID'].unique()
    min_date = df['InvoiceDate'].min()
    max_date = df['InvoiceDate'].max()
    colums = params['featurization']['columns']

    current_date = max_date + pd.DateOffset(days=1)

    customer_id_list = []
    recency_list = []
    frecuency_list = []
    monetary_list = []
    is_churn_list = []

    for customer in customers:
        customer_activity = df[ df['CustomerID'] == customer] 
        last_shopping_day = customer_activity['InvoiceDate'].max()
        last_shopping_day_minus_one_year = last_shopping_day - pd.DateOffset(years=1)
        shopping_activity_last_year = customer_activity[ customer_activity['InvoiceDate'] > last_shopping_day_minus_one_year] 

        # If custumer has more than 1 invoice number
        is_churn = customer_activity['InvoiceNo'].unique().size > 1
        # the number of days of the last purchse
        recency = (current_date - last_shopping_day).days
        # Mean of unique invoicr id in the last year
        frecuency = shopping_activity_last_year['InvoiceNo'].unique().size / 12
        # mean cost total of each invoice in the last year
        monetary = (shopping_activity_last_year['Quantity'] * shopping_activity_last_year['UnitPrice']).mean()

        customer_id_list.append(customer)
        recency_list.append(recency)
        frecuency_list.append(frecuency)
        monetary_list.append(monetary)
        is_churn_list.append(is_churn)


    process_data = list(zip(customer_id_list,recency_list,frecuency_list,monetary_list,is_churn_list))
    df = pd.DataFrame(process_data, columns=colums)

    return df




def process() -> None:
    df_raw = fetch_data()
    df = set_columns_types(df_raw)
    df = make_featurization(df)

    path_featurization_data = params["paths"]["featurization_data"]
    df.to_csv(path_featurization_data, index=False, encoding="utf-8")

    print(
        f"Raw data has {df_raw.shape[0]} rows, prepared data has {df.shape[0]} rows. Difference: {df_raw.shape[0] - df.shape[0]}"
    )

    return df


if __name__ == "__main__":
    process()
