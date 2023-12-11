from agent import mind
from tensorflow import keras
from tensorflow.python import keras
from keras import Sequential
from keras.layers import Dense
from keras.losses import BinaryCrossentropy
from keras.optimizers import Adam

model = Sequential([
	Dense(units=68, activation='sigmoid'),
    Dense(units=32, activation='sigmoid'),
	Dense(units=15, activation='sigmoid'),
    Dense(units=7, activation='sigmoid'),
	Dense(units=1, activation='linear'),
		])

optimizer = Adam(learning_rate=0.05)
model.compile(optimizer=optimizer, loss='mse')

def map_move_to_1D_list(history):
    X_train = []
    Y_train = []
    for move in history:
        # Flatten the matrix into a 1D list and create a set of unique letters
        flat_matrix = [char for row in move[0] for char in row]
        unique_letters = sorted(set(['R', 'H', 'B', 'Q', 'K', 'P', 'r', 'h', 'b', 'q', 'k', 'p', ' ']))
        # Create a dictionary to map letters to integers
        letter_to_integer = {letter: i for i, letter in enumerate(unique_letters)}
        # Map the flattened matrix to a list of integers
        mapped_integers = [letter_to_integer[char] for char in flat_matrix]
        X_row = mapped_integers + [move[1], move[2], move[3], move[4]]
        X_train.append(X_row)
        Y_train.append(move[5])
        #print(f"X_train: {X_train}")
        #print(f"Y_train: {Y_train}")
    return X_train, Y_train

def learn(X_train, Y_train):
    model.fit(X_train, Y_train, epochs=100, batch_size=10)

#Y_test = model.predict(X_test)