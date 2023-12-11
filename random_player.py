# In this file, it is implemented the simple AI-like player which lists the possible moves and randomly chooses one of them
from agent import mind
import random
import copy

LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI

class random_player(mind):
    def update_board(self, arbiter_board):
        self.board = copy.copy(arbiter_board)

    def choose_move(self):
        self.list_possible_moves(True, self.player)
        #self.print_possible_moves()
        if self.player == LOWER:
            N = len(self.possible_moves_lower)
            if N > 0:
                random_move_i = random.randint(0, N-1)
                return self.possible_moves_lower[random_move_i]
        if self.player == UPPER:
            N = len(self.possible_moves_upper)
            if N > 0:
                random_move_i = random.randint(0, N-1)
                return self.possible_moves_upper[random_move_i]
        return [-1, -1, -1, -1]
