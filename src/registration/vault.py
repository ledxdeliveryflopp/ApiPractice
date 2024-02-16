import hvac

client = hvac.Client(
    url='http://vault:8200',
    token='dev-only-token',
)


def create_secret():
    new_secret = client.secrets.kv.v2.create_or_update_secret(
        path=f'password',
        secret=dict(password=f"sdfdsfsdfsdf"),
    )
    return new_secret


def read_secret():
    secret_by_vault = client.secrets.kv.read_secret_version(path=f'password')
    secret = secret_by_vault["data"]["data"]["password"]
    return secret
