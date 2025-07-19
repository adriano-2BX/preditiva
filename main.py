# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# --- Modelos de Dados (para validação de entrada e saída) ---

class TimePoint(BaseModel):
    """Representa um único ponto de dado no tempo."""
    timestamp: datetime
    value: float = Field(..., ge=0, description="O valor da métrica (ex: 85.5 para 85.5% de uso)")

class PredictionRequest(BaseModel):
    """O corpo da requisição para a nossa API de previsão."""
    # Exigimos pelo menos 4 pontos para uma tendência mínima
    history: List[TimePoint] = Field(..., min_length=4)
    capacity: float = Field(100.0, description="A capacidade máxima do recurso.")
    
class PredictionResponse(BaseModel):
    """A resposta que nossa API retornará."""
    trend: str
    slope: float
    estimated_days_until_capacity: float | None
    prediction_date: datetime

# --- Inicia a Aplicação FastAPI ---
app = FastAPI(
    title="API de Análise Preditiva Simples",
    description="Prevê quando um recurso atingirá a capacidade máxima com base em dados históricos."
)

# --- Endpoint de Previsão ---

@app.post("/predict", response_model=PredictionResponse, tags=["Análise Preditiva"])
async def predict_resource_usage(request: PredictionRequest):
    """
    Recebe uma série temporal de dados e prevê o futuro usando Regressão Linear.
    """
    try:
        # 1. Converter os dados de entrada para um DataFrame do Pandas
        df = pd.DataFrame([p.model_dump() for p in request.history])
        
        # Converte o timestamp para um valor numérico (dias desde uma data de referência)
        # para que o modelo de regressão possa usá-lo.
        df['days_ordinal'] = (df['timestamp'] - df['timestamp'].min()).dt.days
        
        # 2. Preparar os dados para o Scikit-learn
        X = df[['days_ordinal']]  # Variável independente (tempo)
        y = df['value']          # Variável dependente (uso do recurso)
        
        # 3. Treinar o modelo de Regressão Linear
        model = LinearRegression()
        model.fit(X, y)
        
        # O 'coeficiente' (slope) nos diz o quanto o recurso aumenta por dia.
        slope = model.coef_[0]
        
        # 4. Fazer a Previsão
        days_until_capacity = None
        trend = "stable"
        
        if slope > 0.01:  # Consideramos uma tendência de crescimento se aumenta mais de 0.01 por dia
            trend = "increasing"
            # Fórmula: Dias = (Valor Desejado - Valor Inicial) / Crescimento por Dia
            # Usamos o 'intercept' como valor inicial na nossa linha de tendência
            remaining_capacity = request.capacity - model.intercept_
            days_from_start = remaining_capacity / slope
            
            # Ajustamos para saber quantos dias faltam a partir de HOJE
            today_ordinal = (datetime.now() - df['timestamp'].min()).days
            days_until_capacity = days_from_start - today_ordinal

        elif slope < -0.01:
            trend = "decreasing"
        
        return {
            "trend": trend,
            "slope": round(slope, 4), # Aumento médio por dia
            "estimated_days_until_capacity": round(days_until_capacity, 1) if days_until_capacity is not None else None,
            "prediction_date": datetime.now()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro durante a análise: {e}")
