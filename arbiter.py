from agent import mind

LOWER = 0 # Human (or AI under training) (Lower) (0)
UPPER = 1 # AI (Upper) (1)
ARBITER = 2

LOWER_VICTORY = 0
UPPER_VICTORY = 1
GAME_NOT_FINISHED = -1
DRAW = -2

class arbiter(mind):
    def make_move(self, i, j, i_new, j_new):
        # makes the move in the arbiter (reference) board
        if self.is_move_valid(i, j, i_new, j_new, True) == 1:
            if self.board[i][j].islower() == True and self.verify_check_after_move(i, j, i_new, j_new, LOWER) == False:
                piece_moved = self.board[i][j]
                points = self.award_points(piece_moved, i_new, j_new)
                self.history.append([self.board, i, j, i_new, j_new, points])
                self.board[i_new][j_new] = piece_moved
                self.board[i][j] = ' '
                # Verify pawn promotion
                if piece_moved == 'p' and i_new == 0:
                    # Code to player choose a piece (queen, bishop, rook or horse). Temporarily setted as queen
                    self.board[i_new][j_new] = 'q'
                return True
            elif self.board[i][j].isupper() == True and self.verify_check_after_move(i, j, i_new, j_new, UPPER) == False:
                piece_moved = self.board[i][j]
                points = self.award_points(piece_moved, i_new, j_new)
                self.history.append([self.board, i, j, i_new, j_new, points])
                self.board[i_new][j_new] = piece_moved
                self.board[i][j] = ' '
                # Verify pawn promotion
                if piece_moved == 'P' and i_new == 7:
                    # Code to player choose a piece (queen, bishop, rook or horse). Temporarily setted as queen
                    self.board[i_new][j_new] = 'Q'
                return True
            else:
                return False
        else:
            return False

    def print_history(self):
        print("Game history:")
        print(self.history)
