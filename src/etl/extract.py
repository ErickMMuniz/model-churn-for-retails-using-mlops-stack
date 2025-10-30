import pandas as pd

def extract_data(path: str):
    """
    Extracts data from a CSV file, handling potential UnicodeDecodeError by trying different encodings.

    Args:
        path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The extracted data as a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='ISO-8859-1')
    return df

def filter_invoices_with_non_negative_quantity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters out invoices where all items have a negative quantity.

    This function identifies invoices that exclusively contain items with negative quantities,
    which typically represent refunds or cancellations. These invoices are then removed
    from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing invoice data.
                           It must have 'InvoiceNo' and 'Quantity' columns.

    Returns:
        pd.DataFrame: The DataFrame with invoices containing only negative quantities removed.
    """

    invoice_ids_with_only_negative_quantity = df.groupby('InvoiceNo').filter(lambda g: (g['Quantity'] < 0).all())['InvoiceNo'].unique()
    df = df[~df['InvoiceNo'].isin(invoice_ids_with_only_negative_quantity)]
    return df

def filter_shop_tiems_with_empty_description_and_zero_unit_price(df: pd.DataFrame) -> pd.DataFrame:
    return df[~(df['Description'].isna() & (df['UnitPrice'] == 0))]


def pipeline_to_churn_model(path: str):
    df = extract_data(path)
    