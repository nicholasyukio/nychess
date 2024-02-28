from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

import agent
import arbiter as arb
import reint_minimax

LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI
ARBITER = 2

LOWER_VICTORY = 0
UPPER_VICTORY = 1
GAME_NOT_FINISHED = -1
DRAW = -2

app = FastAPI()

class Game(BaseModel):
    player_name: str
    game_id: str
    board: List[List[str]]  # List of lists of strings
    move: List[int]  # List of integers with length 4

@app.get("/")
async def read_root():
    return {"Message": "NY Chess AI player engine by Nicholas Yukio"}

@app.get("/leaderboard/")
async def leaderboard():
    return {"Message": "This endpoint will retrieve the leaderboard. It is not implemented yet."}

@app.post("/play/")
async def play(game: Game):
    arbiter = arb.arbiter(ARBITER)
    arbiter.history.clear()
    arbiter.board = game.board
    player_upper = reint_minimax.reint_minimax(UPPER) # AI
    human_move = game.move
    game_status = arbiter.verify_end_of_game()
    if game_status == GAME_NOT_FINISHED:
        if arbiter.make_move(human_move[0], human_move[1], human_move[2], human_move[3]) == False:
            return {"result": "error", "message": "Invalid human move", "board": arbiter.board, "AI move": [-1, -1, -1, -1]}
        else:
            game_status = arbiter.verify_end_of_game()
            if game_status == LOWER_VICTORY:
                return {"result": "ended", "message": "LOWER / PLAYER 0 / WHITE wins", "board": arbiter.board, "AI move": AI_move}
            if game_status == UPPER_VICTORY:
                return {"result": "ended", "message": "UPPER / PLAYER 1 / BLACK wins", "board": arbiter.board, "AI move": AI_move}
            if game_status == DRAW:
                return {"result": "ended", "message": "Game ended with a draw", "board": arbiter.board, "AI move": AI_move}
            player_upper.update_board(arbiter.board)
            AI_move = player_upper.choose_move(arbiter)
            if AI_move[0] != -1:
                if arbiter.make_move(AI_move[0], AI_move[1], AI_move[2], AI_move[3]) == False:
                    return {"result": "error", "message": "Chosen AI move is invalid", "board": arbiter.board, "AI move": AI_move} 
                else:
                    i = AI_move[0]
                    j = AI_move[1]
                    i_new = AI_move[2]
                    j_new = AI_move[3]
                    piece_moved = player_upper.board[i][j]
                    points = player_upper.award_points(piece_moved, i_new, j_new)
                    player_upper.history.append([player_upper.board, i, j, i_new, j_new, points])
                    game_status = arbiter.verify_end_of_game()
                    if game_status == GAME_NOT_FINISHED:
                        return {"result": "continue", "message": "", "board": arbiter.board, "AI move": AI_move}
                    else:
                        if game_status == LOWER_VICTORY:
                            return {"result": "ended", "message": "LOWER / PLAYER 0 / WHITE wins", "board": arbiter.board, "AI move": AI_move}
                        if game_status == UPPER_VICTORY:
                            return {"result": "ended", "message": "UPPER / PLAYER 1 / BLACK wins", "board": arbiter.board, "AI move": AI_move}
                        if game_status == DRAW:
                            return {"result": "ended", "message": "Game ended with a draw", "board": arbiter.board, "AI move": AI_move}
            else:
                return {"result": "error", "message": "Chosen AI move is invalid", "board": arbiter.board, "AI move": AI_move}
    else:
        if game_status == LOWER_VICTORY:
            return {"result": "ended", "message": "LOWER / PLAYER 0 / WHITE wins", "board": arbiter.board, "AI move": [-1, -1, -1, -1]}
        if game_status == UPPER_VICTORY:
            return {"result": "ended", "message": "UPPER / PLAYER 1 / BLACK wins", "board": arbiter.board, "AI move": [-1, -1, -1, -1]}
        if game_status == DRAW:
            return {"result": "ended", "message": "Game ended with a draw", "board": arbiter.board, "AI move": [-1, -1, -1, -1]}