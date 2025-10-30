import numpy as np
import dvc.api
import pandas as pd
import mlflow.sklearn
from mlflow.models import infer_signature
from etl.extract import extract_data
from etl.load import save_metrics
from utils import log_function_call
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
mlflow.set_experiment("churn-model")

params = dvc.api.params_show()

data_url = dvc.api.get_url(
    path=params["paths"]["data"],
    rev=params["training"]['version_data']
)


@log_function_call
def fetch_data() -> pd.DataFrame:
    path_data = params["paths"]["featurization_data"]
    df = extract_data(path_data)
    return df


@log_function_call
def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    random_state = params["variables"]["random_state"]
    test_size = params["variables"]["test_size"]
    train_size = params["variables"]["train_size"]

    features_to_train = params["training"]["columns"]
    target = params["training"]["target"]
    X = df[features_to_train]
    y = df[target]

    return train_test_split(
        X, y, test_size=test_size, train_size=train_size, random_state=random_state
    )


@log_function_call
def balance_data(
    X_train: pd.DataFrame, y_train: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    smote = SMOTE()
    return smote.fit_resample(X_train, y_train)


@log_function_call
def train_model(X_train: pd.DataFrame, y_train: pd.DataFrame) -> LogisticRegression:
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model


@log_function_call
def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.DataFrame) -> pd.DataFrame:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)

    metrics = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC AUC": roc_auc,
    }
    save_metrics(metrics, params["paths"]["metrics_model"])
    return metrics


@log_function_call
def record_model(model, X_train, metrics, params_to_record, df_raw):
    eval_dataset = mlflow.data.from_pandas(
        df_raw,
        source=data_url,
        name=params["paths"]["data"],
        targets=params["training"]["target"][0]
    )

    with mlflow.start_run():
        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(model, artifact_path="models/churn_model", signature=signature)
        mlflow.log_params(params_to_record)
        mlflow.log_metrics(metrics)
        mlflow.log_input(eval_dataset, context="evaluation")
        mlflow.end_run()
       


def process() -> None:
    df_raw = fetch_data()
    X_train, X_test, y_train, y_test = split_data(df_raw)
    # X_train, y_train = balance_data(X_train, y_train)
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    params_to_record = params["training"] | params["variables"] | {"data": data_url}
    record_model(model, X_train, metrics,params_to_record, df_raw)

if __name__ == "__main__":
    process()
