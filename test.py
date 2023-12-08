import requests
from main import PORT

base_url = f"http://127.0.0.1:{PORT}"
username = "akarmain"

# Получаем топ 20 пользователей
response_top_players = requests.get(f"{base_url}/top-players")
print(response_top_players.json())


# Сохраняем результаты игры
result = 1000000
time = "10:00 8.12.23"
response_add_game = requests.post(
    f"{base_url}/games/{username}",
    json={"result": result, "time": time}
)
print(response_add_game)

