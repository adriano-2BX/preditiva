import requests
import time
import json
import os
from datetime import datetime
import mysql.connector

CONFIG_FILE = 'config.json'

def get_db_connection():
    """Lê a configuração e conecta ao banco de dados."""
    if not os.path.exists(CONFIG_FILE):
        print("Ficheiro de configuração não encontrado. Execute o setup pela interface web primeiro.")
        return None
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados no worker: {err}")
        return None

def fetch_weather_data(station_code="A705"):
    """Busca os dados mais recentes da API do INMET."""
    print(f"Worker: Buscando dados da estação {station_code}...")
    try:
        response = requests.get(f"https://apitempo.inmet.gov.br/estacao/dados/{station_code}")
        response.raise_for_status()
        data = response.json()
        latest_data = data[-1]
        return latest_data
    except Exception as e:
        print(f"Worker: Erro ao buscar dados da API: {e}")
        return None

def save_data_to_db(conn, data):
    """Guarda os dados coletados no banco de dados."""
    cursor = conn.cursor()
    sql = ("INSERT INTO dados_meteorologicos (timestamp, temperatura, umidade, chuva_mm_1h, vento_kmh) "
           "VALUES (%s, %s, %s, %s, %s)")
    
    dt_medicao = f"{data['DT_MEDICAO']} {data['HR_MEDICAO'][:2]}:00:00"
    timestamp = datetime.strptime(dt_medicao, '%Y-%m-%d %H:%M:%S')
    
    # Converte valores para float, tratando Nones
    temp = float(data['TEM_INS']) if data['TEM_INS'] else 0.0
    umid = float(data['UMD_INS']) if data['UMD_INS'] else 0.0
    chuva = float(data['CHUVA']) if data['CHUVA'] else 0.0
    vento = float(data['VEN_VEL']) * 3.6 if data['VEN_VEL'] else 0.0 # m/s para km/h

    values = (timestamp, temp, umid, chuva, vento)
    
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    print(f"Worker: Dados guardados no banco. Temperatura: {temp}°C")

def analyze_and_save_alerts(conn):
    """Analisa os dados recentes do DB e guarda alertas."""
    # Esta função seria muito mais complexa, analisando dados por bairro
    # Por enquanto, vamos manter a lógica simples de gerar um alerta fictício
    cursor = conn.cursor()
    
    # Limpa alertas com mais de 24h
    cursor.execute("DELETE FROM alertas_ativos WHERE timestamp < NOW() - INTERVAL 1 DAY")

    # Exemplo: Gera um alerta para o Urbanova se a umidade for muito baixa
    cursor.execute("SELECT umidade FROM dados_meteorologicos ORDER BY timestamp DESC LIMIT 1")
    latest_humidity = cursor.fetchone()
    
    if latest_humidity and latest_humidity[0] < 20:
        sql = ("INSERT INTO alertas_ativos (timestamp, bairro, nivel, descricao) "
               "VALUES (%s, %s, %s, %s)")
        values = (datetime.now(), 'Urbanova', 'ALTO', f'Umidade crítica em {latest_humidity[0]}%. Risco elevado de incêndio.')
        cursor.execute(sql, values)
        print("Worker: Alerta de baixa umidade gerado para o Urbanova.")

    conn.commit()
    cursor.close()

def main_loop():
    """Loop principal do worker."""
    while True:
        conn = get_db_connection()
        if conn:
            data = fetch_weather_data()
            if data:
                save_data_to_db(conn, data)
                analyze_and_save_alerts(conn)
            conn.close()
        else:
            print("Worker: Aguardando configuração do banco de dados...")
        
        print("Worker: Aguardando 30 minutos para o próximo ciclo.")
        time.sleep(1800)

if __name__ == "__main__":
    main_loop()
