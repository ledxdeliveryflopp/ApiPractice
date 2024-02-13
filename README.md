1. Установка [python3.11.3](https://www.get-python.org/downloads/release/python-3113/)
2. Проверить в консоле 
```bash 
python3  
```
3. Создать виртуальное окружение в папке с проектом, пишем в консоле
```bash 
python3 -m venv venv  
```
Должна появиться дериктория venv

4. Активируем вертиульную среду, в консоле
```bash 
source venv/bin/activate 
```
5. Устновим менеджер пакетов Poetry
```bash 
pip install poetry
```
6. Установим зависимости из Poetry
```bash 
poetry update
```
7. Развернем Docker 
```bash 
docker-compose up -d --build <service_name>
```
8. Выполним начальную миграцию
```bash 
alembic revision --autogenerate -m "init"
```
