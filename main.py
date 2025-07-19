# main.py (Versão SIMPLIFICADA para teste)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
# import pandas as pd -> Removido temporariamente
# from sklearn.linear_model import LinearRegression -> Removido temporariamente

class TimePoint(BaseModel):
    timestamp: datetime
    value: float

class PredictionRequest(BaseModel):
    history: List[TimePoint]

class PredictionResponse(BaseModel):
    status: str
    message: str
    data: dict

app = FastAPI(
    title="API de Teste de Build",
    description="Testando o pipeline de deploy com dependências mínimas."
)

@app.post("/predict", response_model=PredictionResponse, tags=["Teste de Build"])
async def predict_resource_usage(request: PredictionRequest):
    """
    Este é um endpoint de teste. Ele não faz nenhuma previsão real.
    Apenas retorna uma resposta estática para confirmar que a API está no ar.
    """
    # A lógica de previsão foi comentada para o teste.
    return {
        "status": "ok",
        "message": "Build com dependências mínimas funcionou com sucesso!",
        "data": {
            "received_points": len(request.history)
        }
    }
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro durante a análise: {e}")
