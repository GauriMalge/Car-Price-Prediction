from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

from .function import load_data, clean_and_prepare_data, process_features
from .ML import predict_car_price
from .Visualization import generate_plots

app = FastAPI(title="Car Price API")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "imports-85.data"

df_processed = None
plots = None

class PredictRequest(BaseModel):
    horsepower: float
    engine_size: float
    curb_weight: float
    city_mpg: float
    fuel_type: str

@app.on_event("startup")
def load_model():
    global df_processed, plots
    df_raw = load_data(DATA_PATH)
    df_clean = clean_and_prepare_data(df_raw)
    df_processed = process_features(df_clean)
    plots = generate_plots(df_processed)

@app.get("/")
def home():
    return {"message": "Car price API is running"}

@app.post("/predict")
def predict(req: PredictRequest):
    result = predict_car_price(
        req.horsepower,
        req.engine_size,
        req.curb_weight,
        req.city_mpg,
        req.fuel_type,
        df_processed
    )
    return {"prediction": result}