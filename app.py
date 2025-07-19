# app.py
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

# -------------------------------------------------------------------
# 1. Carregamento do Modelo
# -------------------------------------------------------------------

# O modelo agora é carregado de um arquivo, não treinado aqui.
model_filename = 'house_price_model.joblib'
model = None

# Bloco de segurança para garantir que o modelo existe.
try:
    model = joblib.load(model_filename)
    print(f"--- Modelo '{model_filename}' carregado com sucesso! ---")
except FileNotFoundError:
    print(f"ERRO: Arquivo do modelo '{model_filename}' não encontrado.")
    # Em um ambiente de produção, você pode querer que a aplicação pare se o modelo não puder ser carregado.
    exit()

# Nomes das colunas na ordem que o modelo espera.
MODEL_FEATURES = ['tamanho_m2', 'quartos', 'idade_anos']


# -------------------------------------------------------------------
# 2. Configuração da Aplicação Flask (API)
# -------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está no ar."""
    status = "OK" if model is not None else "ERRO: Modelo não carregado"
    return f"API de Previsão de Preços de Imóveis. Status do Modelo: {status}"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint que recebe dados de entrada em JSON e retorna a previsão do modelo.
    """
    if model is None:
        return jsonify({'error': 'Modelo não está disponível para fazer previsões.'}), 503

    try:
        # Pega os dados JSON enviados na requisição.
        json_data = request.get_json(force=True)

        # Esperamos um formato como: {"features": [[140, 3, 2], [180, 4, 1]]}
        features = json_data['features']

        # Converte os dados para um DataFrame do Pandas com as colunas corretas.
        prediction_data = pd.DataFrame(features, columns=MODEL_FEATURES)

        # Usa o modelo carregado para fazer a previsão.
        prediction = model.predict(prediction_data)

        # Formata a saída para uma lista de números (arredondando para 2 casas decimais).
        output = [round(p, 2) for p in prediction.tolist()]

        return jsonify({'prediction': output})

    except (KeyError, TypeError, ValueError) as e:
        # Erro mais específico se o JSON estiver mal formatado ou faltando.
        error_msg = f"Erro no formato do input: {e}. O formato esperado é {{'features': [[num, num, num]]}}."
        return jsonify({'error': error_msg}), 400
    except Exception as e:
        # Erro genérico para outros problemas.
        return jsonify({'error': f'Ocorreu um erro inesperado: {str(e)}'}), 500

# -------------------------------------------------------------------
# 3. Execução da Aplicação
# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
