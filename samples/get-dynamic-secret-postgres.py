import hvac
import psycopg2
import os

# URL do Vault e token de autenticação
VAULT_URL = 'http://127.0.0.1:8200'
VAULT_TOKEN = 'your-token'

# Configuração da role e caminho das credenciais
ROLE_NAME = 'read'
CREDENTIALS_PATH = f'database/creds/{ROLE_NAME}'

# Conectar ao Vault
client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)

if not client.is_authenticated():
    print("Erro: Falha na autenticação ao Vault")
    exit(1)

# Obter as credenciais dinâmicas
credentials = client.read(CREDENTIALS_PATH)

if 'data' not in credentials:
    print("Erro: Falha ao obter credenciais do Vault")
    exit(1)

username = credentials['data']['username']
password = credentials['data']['password']

# Conectar ao PostgreSQL usando as credenciais dinâmicas
try:
    conn = psycopg2.connect(
        dbname="usda",
        user=username,
        password=password,
        host="172.21.121.140"
    )
    print("Conexão estabelecida com sucesso")

    # Realizar operações no banco de dados
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT NOW()")
            result = cursor.fetchone()
            print("Hora atual no banco de dados:", result)
            print()
            print("Usuário:", username)
            print("Senha:", password)
            print()
            
            # Testar query simples
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("Teste de conexão bem-sucedido, resultado da query simples:", result)

            # Executar a query desejada com limite aumentado para 10
            cursor.execute("SELECT * FROM public.fd_group LIMIT 10;")
            results = cursor.fetchall()
            print("Resultado da query 'SELECT * FROM public.fd_group' com limite 10:")
            for row in results:
                print(row)

    except psycopg2.Error as e:
        print("Erro ao executar a query no PostgreSQL:", e)

finally:
    if conn:
        conn.close()
        print("Conexão fechada")
