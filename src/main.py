from fastapi import FastAPI
from .model import Model

app = FastAPI()
model = Model()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict(text: str):
    return {"prediction": model.predict(text)}