import json
import mlflow.sklearn


def save_metrics(metrics: dict[str, float], path: str) -> None:
    """
    Saves a dictionary of metrics to a Json file.

    Args:
        metrics (dict[str, float]): A dictionary where keys are metric names and values are their values.
        path (str): The path to the Json file where the metrics will be saved.
    """
    with open(path, "w") as f:
        json.dump(metrics, f)


def save_model(model, path: str) -> None:
    mlflow.sklearn.save_model(sk_model=model, path="my_sklearn_model")
