from fastapi import FastAPI
import mlflow
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
mlflow.set_tracking_uri('http://localhost:5000')

RUN_ID = "YOUR_MLFLOW_RUN_ID"  
# MODEL_URI = f"runs:/{RUN_ID}/models/churn_model" 
MODEL_URI = 'runs:/e70c549c1e244a03b339250bba60b8a6/models/churn_model'
model = mlflow.pyfunc.load_model(MODEL_URI)

class ChurnPredictionRequest(BaseModel):
    Recency: float
    Frequency: float
    Monetary: float

@app.post("/predict")
async def predict_churn(request: ChurnPredictionRequest):
    data = pd.DataFrame([request.dict()])
    prediction = model.predict(data)
    return {"churn_prediction": prediction.tolist()}

@app.get("/")
async def root():
    return {"message": "MLflow Churn Prediction API"}
