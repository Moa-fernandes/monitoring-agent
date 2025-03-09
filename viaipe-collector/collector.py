import requests
import json
import time
import psycopg2
from config import VIAIPE_API_URL, DB_CONFIG

def fetch_data():
    """Obtém os dados da API ViaIpe"""
    try:
        response = requests.get(VIAIPE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Log detalhado dos dados recebidos
        print("🔹 Dados recebidos da API:")
        for client in data[:5]:  # Exibe apenas os 5 primeiros para evitar logs gigantes
            print(json.dumps(client, indent=4, ensure_ascii=False))  # Garante UTF-8 no log

        return data
    except requests.RequestException as e:
        print(f"❌ Erro ao obter dados da API: {e}")
        return []

def process_data(data):
    """Processa os dados para calcular disponibilidade e consumo de banda média"""
    if not data:
        print("⚠️ Nenhum dado recebido da API.")
        return None, None

    print(f"📥 Processando {len(data)} clientes...")

    total_availability = 0
    total_bandwidth = 0
    valid_entries = 0

    for client in data:
        if "data" in client:
            smoke = client["data"].get("smoke", {})
            interfaces = client["data"].get("interfaces", [])

            availability = smoke.get("avg_loss", 0)
            bandwidth = interfaces[0].get("avg_in", 0) if interfaces else 0

            # Garante que os valores são do tipo float
            try:
                availability = float(availability)
                bandwidth = float(bandwidth)
            except ValueError:
                print(f"⚠️ Dados inválidos para {client.get('id', 'Desconhecido')}. Pulando...")
                continue

            print(f"🔍 Cliente: {client.get('id', 'Desconhecido')} | Disponibilidade: {availability} | Banda: {bandwidth}")

            total_availability += availability
            total_bandwidth += bandwidth
            valid_entries += 1

    if valid_entries == 0:
        print("⚠️ Nenhuma entrada válida encontrada para calcular média.")
        return None, None

    avg_availability = total_availability / valid_entries
    avg_bandwidth = total_bandwidth / valid_entries

    print(f"📊 Média calculada - Disponibilidade: {avg_availability:.4f}, Banda: {avg_bandwidth:.2f}")

    return avg_availability, avg_bandwidth

def debug_data(avg_availability, avg_bandwidth):
    """Verifica se os valores estão corretos antes de salvar"""
    print(f"📋 DEBUG: disponibilidade={avg_availability}, banda={avg_bandwidth}")

    try:
        str(avg_availability).encode("utf-8")
        str(avg_bandwidth).encode("utf-8")
        print("✅ Os valores são compatíveis com UTF-8.")
    except UnicodeEncodeError as e:
        print(f"❌ ERRO de codificação nos dados: {e}")

def save_to_db(avg_availability, avg_bandwidth):
    """Salva os dados no banco de dados PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            client_encoding="UTF8"  # Configuração forçada para UTF-8
        )
        cur = conn.cursor()

        print(f"📥 Salvando no banco: disponibilidade={avg_availability}, banda={avg_bandwidth}")

        cur.execute("""
            INSERT INTO viaipe_monitor (availability, bandwidth, timestamp)
            VALUES (%s, %s, NOW())
        """, (float(avg_availability), float(avg_bandwidth)))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Dados salvos no banco de dados.")
    except psycopg2.Error as e:
        print(f"❌ Erro ao salvar no banco: {e}")

if __name__ == "__main__":
    while True:
        data = fetch_data()
        avg_availability, avg_bandwidth = process_data(data)

        if avg_availability is not None and avg_bandwidth is not None:
            debug_data(avg_availability, avg_bandwidth)  # Testa se os valores são válidos antes de salvar
            print(f"📊 Disponibilidade Média: {avg_availability * 100:.2f}%")
            print(f"📡 Consumo Médio de Banda: {avg_bandwidth:.2f} Mbps")
            save_to_db(avg_availability, avg_bandwidth)
        
        time.sleep(60)  # Atualiza a cada minuto
