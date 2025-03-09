import psycopg2
from config import DB_CONFIG

try:
    print("⏳ Tentando conectar ao PostgreSQL...")
    conn = psycopg2.connect(**DB_CONFIG)
    print("✅ Conexão com PostgreSQL bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
