from agent import mind
import random
import numpy as np
from tensorflow import keras
from tensorflow.python import keras
from keras import Sequential
from keras.layers import Dense
from keras.losses import BinaryCrossentropy
from keras.optimizers import Adam
from keras.models import load_model


LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI

valid_move_test = mind(LOWER)

def randomize_board():
    letters = ['R', 'H', 'B' , 'R', 'H', 'B', 'Q', 'K', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'r', 'h', 'b', 'r', 'h', 'b', 'q', 'k', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    for i in range(8):
        for j in range(8):
            N = len(letters)
            random_piece = random.randint(0, N-1)
            valid_move_test.board[i][j] = letters[random_piece]
            letters.pop(random_piece)

def randomize_move():
    i = random.randint(0, 7)
    j = random.randint(0, 7)
    i_new = random.randint(0, 7)
    j_new = random.randint(0, 7)
    return [i, j, i_new, j_new]

def randomize_X_train_Y_train(length: int):
    X_train = []
    Y_train = []
    for k in range(length):
        randomize_board()
        if k % 2 == 0: 
            move = randomize_move()
            while valid_move_test.is_move_valid(move[0], move[1], move[2], move[3]) == 1:
                move = randomize_move()
        else:
            valid_move_test.list_possible_moves(False, LOWER)
            N = len(valid_move_test.possible_moves_lower)
            move_index = random.randint(0, N-1)
            move = valid_move_test.possible_moves_lower[move_index]
        # Flatten the matrix into a 1D list and create a set of unique letters
        flat_matrix = [char for row in valid_move_test.board for char in row]
        unique_letters = sorted(set(['R', 'H', 'B', 'Q', 'K', 'P', 'r', 'h', 'b', 'q', 'k', 'p', ' ']))
        # Create a dictionary to map letters to integers
        letter_to_integer = {letter: i for i, letter in enumerate(unique_letters)}
        # Map the flattened matrix to a list of integers
        mapped_integers = [letter_to_integer[char] for char in flat_matrix]
        X_row = np.array(mapped_integers + [move[0], move[1], move[2], move[3]])
        X_train.append(X_row)
        if valid_move_test.is_move_valid(move[0], move[1], move[2], move[3]) == 1:
            Y_train.append(1)
        else:
            Y_train.append(0)
    X_train = np.array(X_train)
    Y_train = np.array(Y_train)
    #print(f"X_train: {X_train}")
    ones = np.sum(Y_train == 1)
    zeros = np.sum(Y_train == 0)
    print(f"{length} examples generated in the dataset. {ones} ({ones*100/length} %) are equal to 1, and {zeros} ({zeros*100/length} %) are equal to 0")
    return X_train, Y_train

model = load_model("model.keras")
#optimizer = Adam(learning_rate=0.001)
#model.compile(optimizer=optimizer, loss=BinaryCrossentropy(), metrics=['accuracy'])

X_test, Y_ans = randomize_X_train_Y_train(100)
print(f"X_test: {X_test}")
N_test = len(Y_ans)
Y_test = model.predict(X_test)
print(f"Y_ans: {Y_ans}")
print(f"Y_test: {Y_test}")
result_1_1 = 0
result_1_0 = 0
result_0_1 = 0
result_0_0 = 0
for k in range(N_test):
    if Y_test[k] > 0.5:
        if Y_ans[k] == 1:
            result_1_1 += 1
        if Y_ans[k] == 0:
            result_1_0 += 1
    else:
        if Y_ans[k] == 1:
            result_0_1 += 1
        if Y_ans[k] == 0:
            result_0_0 += 1

print(f"{N_test} examples generated in the test set. Results: ")
print(f"{result_1_1} examples CORRECTLY classified by the model as 1")
print(f"{result_1_0} examples WRONGLY classified by the model as 1")
print(f"{result_0_1} examples WRONGLY classified by the model as 0")
print(f"{result_0_0} examples CORRECTLY classified by the model as 0")

