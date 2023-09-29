# Testtask_Incident_collection_system

## Task
Система сбора инцидентов
ручки
POST /problems
нужно сохранить в бд заголовки + body json (других не будет)
вернуть hash всех данных

POST /find
на вход body json ключ значение для поиска в заголовках или body
и нужно вернуть все записи

GET /find2?h=hash
вернуть все записи у который такой hash

================================================================================
по технической части
написать инструкцию как развернуть + docker-compose(чтобы развернуть 1 командой)
критерии по приоритету
1) надежность и целостность данных
2) производительность(скорость ответа)
3) простота(не только кода)

пожелание заказчика
/problems должен максимально быстро принимать данные и вернуть hash
/find должен максимально быстро работать и не отдать кеш

задача со *
у данных 
header
{
    "q": 1,
    "t": 15,
}
body
{
    "hello": "world",
    "z": "6.456",
}

и 

header
{
    "t": 15,
    "q": 1,
}
body
{
    "hello": "world",
    "z": "6.456",
}

должен быть одинаковый hash



## launch
1. Clone project to the desired directory with this command:
    ```
    git clone https://github.com/Daniil7575/Testtask_Incident_collection_system.git
    ```
2. Go to the root folder of *project* (`Testtask_Incident_collection_system`).
3. Add a `.env` file and fill it like this:
    ```
    DB_HOST=db
    DB_PORT=5432
    DB_USER=postgres
    DB_PASS=123
    DB_NAME=incident
    ```
4. Execute below commands:
   ```
   sudo docker compose build
   sudo docker compose up
   ```
5. Go to the `http://127.0.0.1:8000/docs` or `http://0.0.0.0:8000/docs`
