# AI Chess player
# Nicholas Yukio Menezes Sugimoto
# 04 October 2023

import copy
import time
import os
import agent
import arbiter
import random_player
import reint_minimax

game_over = False

LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI
ARBITER = 2

LOWER_VICTORY = 0
UPPER_VICTORY = 1
GAME_NOT_FINISHED = -1
DRAW = -2

# Receiving human input

def get_vector():
    vector = []
    while len(vector) < 4:
        try:
            # Use input() to get user input as a string
            user_input = input(f"Enter element {len(vector) + 1} of the vector: ")
            # Convert the user input to the appropriate data type (e.g., int or float)
            element = int(user_input)  # You can use int() if you want integers
            # Append the element to the vector
            vector.append(element)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return vector

# Here comes the main part of the game

arbiter = arbiter.arbiter(ARBITER)
arbiter.history.clear()
arbiter.print_board()

player_lower = reint_minimax.reint_minimax(LOWER)
player_upper = reint_minimax.reint_minimax(UPPER)

while game_over == False:
    #arbiter.print_board()
    ## makes LOWER move
    if game_over == False:
        #time.sleep(0.5)
        #os.system("clear")
        player_lower.update_board(arbiter.board)
        move = player_lower.choose_move(arbiter)
        if move[0] != -1:
            if arbiter.make_move(move[0], move[1], move[2], move[3]) == False:
                print(f"Invalid LOWER move: {move}")
            else:
                i = move[0]
                j = move[1]
                i_new = move[2]
                j_new = move[3]
                piece_moved = player_lower.board[i][j]
                points = player_lower.award_points(piece_moved, i_new, j_new)
                player_lower.history.append([player_lower.board, i, j, i_new, j_new, points])
                print(f"LOWER Move: {move}")
        else:
            print("Error!")
        arbiter.print_board()
        #arbiter.print_history()
        game_status = arbiter.verify_end_of_game()
        if game_status == GAME_NOT_FINISHED:
            game_over = False
        else:
            game_over = True
        print(f"Number of moves: {len(arbiter.history)}")
        #input("Press Enter to continue...")
    ## makes UPPER move
    if game_over == False:
        #time.sleep(0.5)
        #os.system("clear")
        player_upper.update_board(arbiter.board)
        move = player_upper.choose_move(arbiter)
        if move[0] != -1:
            if arbiter.make_move(move[0], move[1], move[2], move[3]) == False:
                print(f"Invalid UPPER move: {move}")
            else:
                i = move[0]
                j = move[1]
                i_new = move[2]
                j_new = move[3]
                piece_moved = player_upper.board[i][j]
                points = player_upper.award_points(piece_moved, i_new, j_new)
                player_upper.history.append([player_upper.board, i, j, i_new, j_new, points])
                print(f"UPPER move: {move}")
        else:
            print("Error!")
        arbiter.print_board()
        #arbiter.print_history()
        game_status = arbiter.verify_end_of_game()
        if game_status == GAME_NOT_FINISHED:
            game_over = False
        else:
            game_over = True
        print(f"Number of moves: {len(arbiter.history)}")
        #input("Press Enter to continue...")

if game_status == LOWER_VICTORY:
    print("LOWER / PLAYER 0 / WHITE wins!")
if game_status == UPPER_VICTORY:
    print("UPPER / PLAYER 1 / BLACK wins!")
if game_status == DRAW:
    print("The game ended with a draw!")

