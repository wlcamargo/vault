import hvac
import sys

wallace_client = hvac.Client(
    url='http://127.0.0.1:8200',
)
wallace_client.auth.userpass.login(
    username='wallace',
    password='123'
)

# Tentando ler a secret com o token do usuário wallace
try:
    read_response = wallace_client.secrets.kv.v2.read_secret_version(path='my-secret-password')
    password = read_response['data']['data']['password']
    if password == 'Hashi123':
        print('Access granted! Password:', password)
    else:
        print('Unexpected password')
except Exception as e:
    print(f'Error reading secret: {e}')
