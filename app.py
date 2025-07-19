# app.py
# Importando as bibliotecas necessárias
from flask import Flask, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# -------------------------------------------------------------------
# 1. Preparação do Modelo de Machine Learning
# -------------------------------------------------------------------

# Em um cenário real, você carregaria seus dados de um arquivo (ex: CSV)
# ou banco de dados. Para este exemplo, vamos criar dados fictícios.
#
# Objetivo do modelo: Prever o preço de um imóvel (y) com base no seu tamanho em m² (X).
X_train_data = {
    'tamanho_m2': [50, 60, 70, 80, 100, 120, 150]
}
y_train_data = {
    'preco_reais': [150000, 180000, 210000, 240000, 300000, 360000, 450000]
}

# Convertendo os dados para DataFrames do Pandas, que é o formato
# comumente usado em análise de dados com Python.
X_train = pd.DataFrame(X_train_data)
y_train = pd.DataFrame(y_train_data)

# Criando uma instância do modelo de Regressão Linear.
# Este é um dos modelos mais simples de machine learning.
model = LinearRegression()

# Treinando o modelo com nossos dados fictícios.
# O método .fit() "aprende" a relação entre o tamanho (X) e o preço (y).
model.fit(X_train, y_train)

print("--- Modelo de Machine Learning treinado com sucesso! ---")
print(f"Coeficiente (preço por m²): {model.coef_[0][0]:.2f}")
print(f"Intercepto (custo base): {model.intercept_[0]:.2f}")
print("---------------------------------------------------------")


# -------------------------------------------------------------------
# 2. Configuração da Aplicação Flask (API)
# -------------------------------------------------------------------

# Inicializando a aplicação Flask.
app = Flask(__name__)

# Definindo a rota principal da API (opcional, bom para teste de saúde)
@app.route('/', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está no ar."""
    return "API de Previsão está funcionando!"

# Definindo a rota de previsão.
# Usamos o método POST, pois o cliente enviará dados para a API.
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint que recebe dados de entrada em JSON e retorna a previsão do modelo.
    """
    try:
        # 1. Pega os dados JSON enviados na requisição.
        json_data = request.get_json(force=True)

        # 2. Extrai os 'features' (características) do JSON.
        # Esperamos um formato como: {"features": [[110], [130]]}
        # onde cada lista interna é um dado para prever.
        features = json_data['features']

        # 3. Converte os dados para um formato que o modelo entende (DataFrame do Pandas).
        # É importante que a coluna tenha o mesmo nome usado no treinamento ('tamanho_m2').
        prediction_data = pd.DataFrame(features, columns=['tamanho_m2'])

        # 4. Usa o modelo treinado para fazer a previsão.
        prediction = model.predict(prediction_data)

        # 5. Formata a saída para ser uma lista de números.
        output = prediction.flatten().tolist()

        # 6. Retorna a previsão em formato JSON com status 200 (OK).
        return jsonify({'prediction': output})

    except Exception as e:
        # Em caso de erro (ex: JSON mal formatado), retorna uma mensagem de erro.
        return jsonify({'error': str(e)}), 400

# -------------------------------------------------------------------
# 3. Execução da Aplicação
# -------------------------------------------------------------------

# Este bloco garante que o servidor só será executado quando o script
# for chamado diretamente (e não quando for importado por outro script).
if __name__ == '__main__':
    # O host '0.0.0.0' é essencial para que a aplicação seja acessível
    # de fora do container Docker no Easypanel.
    app.run(host='0.0.0.0', port=5000)

