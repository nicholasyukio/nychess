import json
import random
import string
from datetime import datetime

def generate_game_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def write_chess_game_json(game_id, start_time, last_update_time, game_board, game_history, intended_future_moves, game_situation):
    filename = f"game_{game_id}.json"
    data = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "last_update_time": last_update_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "game_board": game_board,
        "game_history": game_history,
        "intended_future_moves": intended_future_moves,
        "game_situation": game_situation
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))
    return game_id

def read_chess_game_json(game_id):
    filename = f"game_{game_id}.json"
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S UTC")
        last_update_time = datetime.strptime(data["last_update_time"], "%Y-%m-%d %H:%M:%S UTC")
        game_board = data["game_board"]
        game_history = data["game_history"]
        intended_future_moves = data["intended_future_moves"]
        game_situation = data["game_situation"]   
    except:
        start_time = datetime.utcnow()
        last_update_time = datetime.utcnow()
        game_board = (
        [['R', 'H', 'B', 'Q', 'K', 'B', 'H', 'R'],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
         ['r', 'h', 'b', 'q', 'k', 'b', 'h', 'r']]
         )
        game_history = []
        intended_future_moves = []
        game_situation = "not_found"
        print(f"File {filename} not found.")
    return start_time, last_update_time, game_board, game_history, intended_future_moves, game_situation

# Example usage:
""" start_time = datetime.utcnow()
last_update_time = datetime.utcnow()
game_history = [[0, 1, 0, 2], [2, 3, 4, 5], [4, 4, 5, 5]]
intended_future_moves = [[0, 1, 0, 2], [2, 3, 4, 5], [4, 4, 5, 5]]
game_situation = "ongoing" """

#write_chess_game_json(game_id, start_time, last_update_time, game_board, game_history, intended_future_moves, game_situation)

# Example usage:
""" game_id = "w7FJYe"
start_time, last_update_time, game_history, intended_future_moves, game_situation = read_chess_game_json(game_id)
print("Start Time:", start_time)
print("Last Update Time:", last_update_time)
print("Game History:", game_history)
print("Intended Future Moves:", intended_future_moves)
print("Game Situation:", game_situation) """