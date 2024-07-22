import hvac

# Autenticação
client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='your-token',
)

# Definindo a política
policy_name = 'wallace-policy'
policy = """
path "secret/my-secret-password" {
  capabilities = ["read"]
}
"""

# Criando a política no Vault
client.sys.create_or_update_policy(
    name=policy_name,
    policy=policy,
)

print(f'Policy {policy_name} created successfully.')

# Criando um token com a política e associando ao usuário wallace
create_token_response = client.auth.token.create(
    policies=[policy_name],
    display_name='wallace'
)

wallace_token = create_token_response['auth']['client_token']
print(f'Token for wallace: {wallace_token}')
