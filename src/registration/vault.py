import hvac

client = hvac.Client(
    url='http://vault:8200',
    token='dev-only-token',
)


async def create_secret(email: str, password: str):
    new_secret = client.secrets.kv.v2.create_or_update_secret(
        path=f'{email}-secret-password',
        secret=dict(password=f"{password}"),
    )
    return new_secret


async def read_secret(email: str):
    secret_by_vault = client.secrets.kv.read_secret_version(path=f'{email}-secret-password')
    secret = secret_by_vault["data"]["data"]["password"]
    return secret
