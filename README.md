# model-churn-for-retails-using-mlops-stack
A challenge to create a simple workflow for develop a churn model. 

## Install env with conda
```bash
conda env create -f environment.yaml
```

## MLflow Model Serving
To deploy the model using MLflow Model Serving, run:
```bash
mlflow server --host 127.0.0.1 --port 8080
```

### Reproducing the DVC Pipeline
To reproduce the data version control (DVC) pipeline and ensure all data processing and model training steps are executed, use:
```bash
dvc repro
```

### Deploying the FastAPI Application
To deploy the churn prediction model as a FastAPI application, navigate to the `app` directory and run:
```bash
uvicorn app.main:app --reload
```

## Future Fixes and Improvements

- **Automated CI/CD Pipeline**: Implement a CI/CD pipeline (e.g., GitHub Actions, GitLab CI) to automate testing, building, and deployment of the model and application.
- **Scalability**: Explore options for scaling the FastAPI application (e.g., Docker Swarm, Kubernetes) for handling increased traffic.
- **Data Versioning for Features**: Extend DVC to version not just raw data but also processed features used for model training.
- **Automated Retraining**: Implement a mechanism for automated model retraining based on performance degradation or new data availability.
- **A/B Testing**: Set up A/B testing infrastructure to compare different model versions in production.
- **Security**: Implement authentication and authorization for the FastAPI application and MLflow server.


# EDA for Churn Model

Summary:
- The database is a time serie about shopping stream.
- The first record is on December 2010. The duration of the record is one year.

Assumptions:
- There is a relation between CustomerId and InvoiceId. One custuomber may have more of one Invoice.
- A Invoice can contain more of one record (each entry in the db is a shop record)
- Quantity and UnitPrice are columns with positive values.
- InvoiceId is a primary key from antother table. 

Problems:
1) There are some items with empty CustomerId, but InvoiceID is well formed. This cases represents around 20 %
2) There are cases with Description is empty. This case is around the 1454 / 541909 * 100 ≃ 0.002 percent of the data.
3) There are ~10 K cases when Quantify is negative. Some cases represents discounts.
4) There are cases when UnitPice is lower to zero
   

Fixes:
1) Fill empty CustomerId checking the relates CustomerId from InvoiceId. This process is like a group by Invoice Id. Apply the following rules:
   - Delete rows when CustomerId is empty or nan.
   - Groupded by InvoiceId.
       - If exists more than one CustomerID, then ignored
       - In another case, fill te CustomerId with that Customer
2) Delete cases when Description is Empty
3) Some cases represents discounts. Follow the next rules:
   - If a invoice only contains shops items with negative unit prices, then is a refund case. In this cases, drop that invoice.
   - Then, a valid Invoice for this model, only ocurrs when a Invoice contains neative or positive values. 