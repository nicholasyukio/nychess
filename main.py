# AI Chess player
# Nicholas Yukio Menezes Sugimoto
# 04 October 2023

import copy
import time
import os
import agent
import arbiter
import random_player
import train_neural_network

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

player_lower = random_player.random_player(LOWER)
player_upper = random_player.random_player(UPPER)

while game_over == False:
    #arbiter.print_board()
    ## makes LOWER move
    if game_over == False:
        #time.sleep(0.5)
        os.system("cls")
        player_lower.update_board(arbiter.board)
        move = player_lower.choose_move()
        if move[0] != -1:
            if arbiter.make_move(move[0], move[1], move[2], move[3]) == False:
                print("Invalid move. Check code.")
        else:
            print("Error!")
        arbiter.print_board()
        #arbiter.print_history()
        if arbiter.verify_end_of_game() == GAME_NOT_FINISHED:
            game_over = False
        else:
            game_over = True
        #input("Press Enter to continue...")
    ## makes UPPER move
    if game_over == False:
        #time.sleep(0.5)
        os.system("cls")
        player_upper.update_board(arbiter.board)
        move = player_upper.choose_move()
        if move[0] != -1:
            if arbiter.make_move(move[0], move[1], move[2], move[3]) == False:
                print("Invalid move. Check code.")
        else:
            print("Error!")
        arbiter.print_board()
        #arbiter.print_history()
        if arbiter.verify_end_of_game() == GAME_NOT_FINISHED:
            game_over = False
        else:
            game_over = True
        #input("Press Enter to continue...")

# Learn with the awarded points
print(f"Number of moves: {len(arbiter.history)}")
X_train, Y_train = train_neural_network.map_move_to_1D_list(arbiter.history)
train_neural_network.learn(X_train, Y_train)
