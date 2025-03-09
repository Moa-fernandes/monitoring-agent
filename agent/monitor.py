import time
import requests
import ping3
import psycopg2
from config import SITES, DB_CONFIG

def get_connection():
    """Cria uma conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            client_encoding="UTF8"
        )
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return None

def ping_test(host):
    """Realiza o ping e retorna latência"""
    try:
        latency = ping3.ping(host) * 1000  # Convertendo para ms
        return latency if latency else None
    except Exception as e:
        print(f"❌ Erro no ping para {host}: {e}")
        return None

def check_website(url):
    """Verifica tempo de resposta e código HTTP"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        elapsed_time = (time.time() - start_time) * 1000  # Convertendo para ms
        return elapsed_time, response.status_code
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return None, None

def save_to_db(host, latency, load_time, status_code):
    """Salva os dados no banco de dados"""
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO network_monitor (host, latency, load_time, status_code, timestamp)
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (host, latency, load_time, status_code)
        )
        conn.commit()
        cur.close()
        print(f"✅ Dados salvos para {host}: Latência {latency}ms, Tempo {load_time}ms, Status {status_code}")
    except Exception as e:
        print(f"❌ Erro ao inserir no banco: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        for site in SITES:
            latency = ping_test(site)
            load_time, status_code = check_website(f"https://{site}")
            save_to_db(site, latency, load_time, status_code)
        time.sleep(60)
