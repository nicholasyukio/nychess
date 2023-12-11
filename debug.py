# AI Chess player
# Nicholas Yukio Menezes Sugimoto
# 04 October 2023

import copy
import time
import os
import agent
import arbiter
import random_player

game_over = False

LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI
ARBITER = 2

LOWER_VICTORY = 0
UPPER_VICTORY = 1
GAME_NOT_FINISHED = -1
DRAW = -2

arbiter = arbiter.arbiter(ARBITER)
arbiter.history.clear()


player_lower = random_player.random_player(LOWER)
player_upper = random_player.random_player(UPPER)

arbiter.board = (
        [[' ', 'H', ' ', ' ', ' ', ' ', ' ', 'k'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', 'R', ' ', ' ', 'K', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P']]
         )

arbiter.print_board()

arbiter.list_possible_moves(True, UPPER)
print("Possible moves for UPPER:")
print(arbiter.possible_moves_upper)

arbiter.list_possible_moves(True, LOWER)
print("Possible moves for LOWER:")
print(arbiter.possible_moves_lower)

if arbiter.verify_check(UPPER) == 0:
    check = False
else:
    check = True
print(f"Check result for UPPER: {check}")

if arbiter.verify_check(LOWER) == 0:
    check = False
else:
    check = True
print(f"Check result for LOWER: {check}")