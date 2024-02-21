1. перейти по http://localhost:8200/ui/ и сделать токены.


3. Разлокировать хранилище с помощью токенов


4. Перейти в secrets и создать secret engine


5. Загрузим файл с политикой токенов
```bash 
vault policy write app_policy policy.hcl
```

6. Создадим токен
```bash 
vault token create -policy=app_policy
```

