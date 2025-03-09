import psycopg2
from psycopg2 import pool

# Configurações do banco de dados
DB_CONFIG = {
    "dbname": "monitoring",
    "user": "user",  # Substitua pelo usuário correto
    "password": "password",  # Substitua pela senha correta
    "host": "postgres",  # Use 'localhost' se não estiver rodando via Docker
    "port": "5432"
}

# Criando um pool de conexões para evitar abrir e fechar conexões constantemente
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10, **DB_CONFIG
    )

    if connection_pool:
        print("✅ Pool de conexões criado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
    connection_pool = None


def get_connection():
    """Obtém uma conexão do pool."""
    try:
        if connection_pool:
            return connection_pool.getconn()
        else:
            raise Exception("Pool de conexões não está disponível.")
    except Exception as e:
        print(f"❌ Erro ao obter conexão: {e}")
        return None


def release_connection(conn):
    """Libera uma conexão de volta para o pool."""
    if connection_pool and conn:
        connection_pool.putconn(conn)


def close_all_connections():
    """Fecha todas as conexões do pool."""
    if connection_pool:
        connection_pool.closeall()
        print("✅ Todas as conexões foram fechadas.")


# Teste de conexão ao rodar o script diretamente
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Conexão obtida com sucesso!")
        release_connection(conn)
