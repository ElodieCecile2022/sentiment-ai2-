from fastapi import FastAPI
from src.schemas import PredictionRequest, PredictionResponse
from src.model import SentimentModel

# Initialisation de l'application FastAPI et du modèle
app = FastAPI(title="Sentiment Analysis API")
model = SentimentModel()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API d'analyse de sentiment"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Appel de la méthode predict du modèle
    result = model.predict(request.text)
    return result