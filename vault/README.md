1. Перейдем по http://<url:host>/ui/ и сделаем токены.


3. Разблокируем хранилище с помощью токенов.


4. Перейдем в secrets и создадим secret engine.


5. Загрузим файл с политикой токенов.
```bash 
vault policy write app_policy policy.hcl
```

6. Создадим токен для приложения.
```bash 
vault token create -policy=app_policy
```

