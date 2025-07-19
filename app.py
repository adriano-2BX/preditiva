from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

CONFIG_FILE = 'config.json'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def check_setup():
    """Verifica se o ficheiro de configuração existe."""
    return os.path.exists(CONFIG_FILE)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Página de instalação para configurar o banco de dados."""
    if check_setup():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        db_config = {
            'host': request.form['host'],
            'user': request.form['user'],
            'password': request.form['password'],
            'database': request.form['database']
        }

        try:
            # Testa a conexão
            conn = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            cursor = conn.cursor()
            
            # Cria o banco de dados se não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']} DEFAULT CHARACTER SET 'utf8'")
            print(f"Banco de dados '{db_config['database']}' garantido.")
            
            # Guarda a configuração
            with open(CONFIG_FILE, 'w') as f:
                json.dump(db_config, f)
            
            # Conecta novamente, agora ao banco de dados específico
            conn.database = db_config['database']
            
            # Cria as tabelas
            create_tables(conn)

            return redirect(url_for('dashboard'))

        except mysql.connector.Error as err:
            return render_template('setup.html', error=f"Erro de configuração: {err}")

    return render_template('setup.html')

def create_tables(conn):
    """Cria as tabelas necessárias no banco de dados."""
    cursor = conn.cursor()
    tables = {}
    tables['dados_meteorologicos'] = (
        "CREATE TABLE `dados_meteorologicos` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `timestamp` datetime NOT NULL,"
        "  `temperatura` float,"
        "  `umidade` float,"
        "  `chuva_mm_1h` float,"
        "  `vento_kmh` float,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    tables['alertas_ativos'] = (
        "CREATE TABLE `alertas_ativos` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `timestamp` datetime NOT NULL,"
        "  `bairro` varchar(100) NOT NULL,"
        "  `nivel` varchar(50) NOT NULL,"
        "  `descricao` text NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print(f"Criando tabela: {table_name}")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Tabela {table_name} já existe.")
            else:
                print(err.msg)
    cursor.close()
    conn.close()

@app.route('/')
def dashboard():
    """Renderiza a página principal do painel."""
    if not check_setup():
        return redirect(url_for('setup'))
    return render_template('dashboard.html')

@app.route('/api/regional_alerts')
def api_alerts():
    """Endpoint da API que fornece os dados de alerta para o mapa a partir do banco."""
    if not check_setup():
        return jsonify({"error": "Aplicação não configurada"}), 500
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500
        
    cursor = conn.cursor(dictionary=True)
    # Busca apenas os alertas das últimas 24 horas
    cursor.execute("SELECT bairro, nivel, descricao FROM alertas_ativos WHERE timestamp >= NOW() - INTERVAL 1 DAY")
    
    alerts_from_db = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Formata os dados para o formato esperado pelo frontend
    formatted_alerts = {row['bairro']: {'nivel': row['nivel'], 'descricao': row['descricao']} for row in alerts_from_db}
    
    return jsonify(formatted_alerts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
