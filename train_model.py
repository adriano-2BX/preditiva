# train_model.py
import pandas as pd
import xgboost as xgb
import joblib

print("--- Iniciando o processo de treinamento do modelo ---")

# 1. Dados de Treinamento
# Agora com múltiplas características (features) para uma previsão mais precisa.
training_data = {
    'tamanho_m2': [120, 150, 80, 200, 100, 135, 250, 95],
    'quartos':    [3, 4, 2, 4, 3, 3, 5, 2],
    'idade_anos': [5, 2, 10, 1, 8, 4, 3, 12],
    'preco_reais': [350000, 480000, 250000, 650000, 290000, 410000, 750000, 275000]
}
df = pd.DataFrame(training_data)

# Separando as características (X) do alvo (y)
X_train = df[['tamanho_m2', 'quartos', 'idade_anos']]
y_train = df['preco_reais']

print("Dados de treinamento carregados:")
print(df)

# 2. Treinamento do Modelo
# Usando o XGBoost Regressor, um modelo mais poderoso.
# Parâmetros como n_estimators e learning_rate podem ser ajustados (tunning).
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)

print("\n--- Treinando o modelo XGBoost... ---")
model.fit(X_train, y_train)
print("--- Treinamento concluído. ---")

# 3. Salvando o Modelo Treinado
# Usamos a biblioteca joblib para salvar o objeto do modelo em um arquivo.
# Este arquivo será carregado pela nossa API.
model_filename = 'house_price_model.joblib'
joblib.dump(model, model_filename)

print(f"\nModelo salvo com sucesso como '{model_filename}'")
