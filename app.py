# app.py
from flask import Flask, request, jsonify, render_template
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# -------------------------------------------------------------------
# 1. Preparação do Modelo de Machine Learning (Versão Simples)
# -------------------------------------------------------------------
# Voltamos ao modelo de Regressão Linear, que é leve e não requer compilação.
# Objetivo: Prever o preço de um imóvel (y) com base no seu tamanho em m² (X).
X_train_data = {
    'tamanho_m2': [50, 60, 70, 80, 100, 120, 150]
}
y_train_data = {
    'preco_reais': [150000, 180000, 210000, 240000, 300000, 360000, 450000]
}

X_train = pd.DataFrame(X_train_data)
y_train = pd.DataFrame(y_train_data)

model = LinearRegression()
model.fit(X_train, y_train)

print("--- Modelo de Regressão Linear treinado com sucesso! ---")

# -------------------------------------------------------------------
# 2. Configuração da Aplicação Flask (API + Interface Gráfica)
# -------------------------------------------------------------------
app = Flask(__name__)

# Rota principal que serve a interface gráfica (o nosso ficheiro index.html)
@app.route('/', methods=['GET'])
def home():
    """
    Serve a página principal com a interface gráfica para o utilizador.
    """
    # O Flask procura automaticamente por 'index.html' na pasta 'templates'.
    return render_template('index.html')

# Rota de previsão que será chamada pela interface gráfica
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint que recebe dados de entrada em JSON e retorna a previsão do modelo.
    """
    try:
        json_data = request.get_json(force=True)
        
        # A nossa interface enviará: {"features": [[tamanho]]}
        features = json_data['features']
        
        prediction_data = pd.DataFrame(features, columns=['tamanho_m2'])
        
        prediction = model.predict(prediction_data)
        
        output = prediction.flatten().tolist()
        
        return jsonify({'prediction': output})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# -------------------------------------------------------------------
# 3. Execução da Aplicação
# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
