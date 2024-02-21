1. Установим менеджер пакетов Poetry.
```bash 
pip install poetry
```

2. Перейдем в src/settings/settings.py и установим нужные значения.


3. Создадим контейнеры .
```bash 
docker compose up -d
```

4. Перейдем в контейнер "authorization" и выполним миграции.
```bash 
alembic revision --autogenerate -m "init"

elembic upgrade head
```

5. Перейдем в контейнер vault и инициализируем его. (Сохраните токены)
```bash 
vault operator init
```

6. Разблокируем хранилище токенами
```bash 
vault operator unseal
```

7. Пройдем аунтификацию с помощью root токена.
```bash 
vaul login
```

7. Загрузим правила доступа для токена.
```bash 
vault policy write app_policy policy.hcl
```

8. Создадим токен для приложения
```bash 
vault token create -policy=app_policy
```

9. Сохраним токен в src/settings/settings.py в переменную vault_token
```bash 
vault token create -policy=app_policy
```

9. Создадим хранилище секретов.
```bash 
vault secrets enable -path=<Название хранилища> kv
```

10. Сохраним путь к хранилищу в src/settings/settings.py в переменную vault_mount