from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List, Optional

app = FastAPI()
PORT = 3031


# Модель для данных игры
class Game(BaseModel):
    result: int
    time: str


# Модель для данных пользователя
class User(BaseModel):
    password: str
    games: List[Game] = []


# Загрузка данных из файла
def load_data():
    try:
        with open('database.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Сохранение данных в файл
def save_data(data):
    with open('database.json', 'w') as file:
        json.dump(data, file, indent=2)


# Получение топ-20 игроков
@app.get("/top-players")
def get_top_players():
    data = load_data()
    top_players = []
    for user, user_data in data.items():
        best_game = max(user_data['games'], key=lambda x: x['result'], default=None)
        if best_game:
            top_players.append((user, best_game['result'], best_game['time']))
    top_players.sort(key=lambda x: x[1], reverse=True)
    return top_players[:20]


# Добавление результата игры для пользователя
@app.post("/games/{username}")
def add_game(username: str, game: Game):
    data = load_data()

    # Создаём пользователя, если он не существует
    if username not in data:
        data[username] = {"password": "", "games": []}

    data[username]['games'].append(game.dict())
    save_data(data)
    return {"message": "Game added successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
