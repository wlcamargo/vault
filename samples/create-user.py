import hvac

# Autenticação como root
client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='your-token',
)
print('connected on vault server!')

# Criando a secret
client.secrets.kv.v2.create_or_update_secret(
    path='my-secret-password',
    secret=dict(password='Hashi123'),
)
print('Secret created successfully.')

# Definindo a política
policy_name = 'wallace-policy'
policy = """
path "secret/data/my-secret-password" {
  capabilities = ["read"]
}
"""
client.sys.create_or_update_policy(
    name=policy_name,
    policy=policy,
)
print(f'Policy {policy_name} created successfully.')

# Criando o usuário
client.auth.userpass.create_or_update_user(
    username='wallace',
    password='123',
    policies=[policy_name],
    metadata={"name": "wallace", "email": "wallacecpdg@gmail.com"}
)
print('User wallace created successfully.')

# Autenticando como o usuário wallace
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
