1. Перейдем по http://<url:host>/ui/ и сделаем токены.


2. Разблокируем хранилище с помощью токенов.


3. Перейдем в secrets и создадим secret engine.


4. Загрузим файл с политикой токенов.
```bash 
vault policy write app_policy policy.hcl
```

5. Создадим токен для приложения.
```bash 
vault token create -policy=app_policy
```

