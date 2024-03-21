# In this file, it is implemented an intelligent version of a player which uses the minimax algorithm to choose the best move
from agent import mind
import random
import copy

LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI
ARBITER = 2 # Arbiter
SCORE_GAIN_THRESHOLD = 10
VALUE_GAIN_THRESHOLD = 10
RETREAT_PENALTY = 100
NUMBER_OF_MOVES_OPENING_PHASE = 7

class reint_minimax(mind):
    def update_board(self, arbiter_board):
        self.board = copy.copy(arbiter_board)
    
    def choose_randomly(self, list):
        return random.choice(list)
    
    def choose_opening_move(self, arbiter):
        game_history = arbiter.history
        number_of_moves = len(game_history)
        if number_of_moves == 0:
            # In this case, the player has to make the first move
            random_sequence = random.choice(self.classic_openings)
            first_move = random_sequence[0]
            #print(f"First move: {first_move}")
            return first_move
        else:
            # In this case, the player has to identify a suitable opening to continue the defense
            selected_openings = copy.copy(self.classic_openings)
            filtered_openings = []
            #print(f"Len of Selected openings: {len(selected_openings)}")
            # This messes with the list and then the for loop does not work properly
            for opening in selected_openings:
                if len(opening) > number_of_moves + 1:
                    filtered_openings.append(opening)
                    #print(f"Opening included: {opening}")
            selected_openings = copy.copy(filtered_openings)
            filtered_openings = []
            #print(f"Len of Selected openings (filtered): {len(selected_openings)}")
            for index in range(number_of_moves):
                for opening in selected_openings:
                    #print(f"index: {index} opening: {opening} game_history: {game_history}")
                    if opening[index] == game_history[index][1:5]:
                        filtered_openings.append(opening)
                selected_openings = copy.copy(filtered_openings)
                filtered_openings = []
            #print(f"Len of Selected openings (Final filter): {len(selected_openings)}")
            if len(selected_openings) == 0:
                return [-1, -1, -1, -1]
            else:
                print(f"Selected openings: {selected_openings}")
                random_sequence = random.choice(selected_openings)
                return random_sequence[number_of_moves]

    def choose_move(self, arbiter):
        game_history = arbiter.history
        number_of_moves = len(game_history)
        self.list_possible_moves(True, self.player)
        #self.print_possible_moves()
        if self.player == LOWER:
            # Checks if the game is in the opening phase
            if number_of_moves < NUMBER_OF_MOVES_OPENING_PHASE:
                opening_move = self.choose_opening_move(arbiter)
                print(f"Opening move: {opening_move}")
                if opening_move[0] != -1:
                    print(f"Best move for opening: {opening_move}")
                    return opening_move
            # First, check immediate rewards or threats
            initial_score = self.score()
            initial_value = self.value()
            min_score_gain = +999999
            min_value_gain = +999999
            for move in self.possible_moves_lower:
                # temporarily change the board to list the possible adversary moves
                i = move[0]
                j = move[1]
                i_new = move[2]
                j_new = move[3]
                piece = self.board[i][j]
                piece_new = self.board[i_new][j_new]
                is_move_a_retreat = self.verify_reverse_moves(i, j, i_new, j_new)
                self.board[i_new][j_new] = self.board[i][j]
                self.board[i][j] = ' '
                self.list_possible_moves(True, self.player)
                new_score = self.score()
                new_value = self.value()
                # returns the board to its previous position
                self.board[i][j] = piece
                self.board[i_new][j_new] = piece_new
                self.list_possible_moves(True, self.player)
                # determine gains
                score_gain = new_score - initial_score
                value_gain = new_value - initial_value
                if is_move_a_retreat == True:
                    score_gain += RETREAT_PENALTY
                    value_gain += RETREAT_PENALTY
                if score_gain < min_score_gain:
                    min_score_gain = score_gain
                    best_move_for_score = move
                if value_gain < min_value_gain:
                    min_value_gain = value_gain
                    best_move_for_value = move
            # Here we decide what to do based on the gains (score and value)
            if min_score_gain < -SCORE_GAIN_THRESHOLD:
                print(f"Best move for score: {best_move_for_score}")
                return best_move_for_score
            #if min_value_gain < -VALUE_GAIN_THRESHOLD:
            else:
                print(f"Best move for value: {best_move_for_value}")
                return best_move_for_value
        """             # If no immediate rewards or threats, then check the best move using the minimax algorithm
                    if len(self.intended_future_moves) > 1:
                        print(f"Intended future move: {self.intended_future_moves[0][0]}")
                        next_move = self.intended_future_moves.pop(0)
                        self.intended_future_moves.pop(0)
                        return next_move[0]
                    # If no intended future moves, then check the best move using the minimax algorithm
                    sc = self.minimax(3, -999999, +999999, LOWER, LOWER)
                    print(f"Best move for minimax: {sc[0]}")
                    self.intended_future_moves.extend(sc[2:])
                    return sc[0][0] """
        if self.player == UPPER:
            # Checks if the game is in the opening phase
            if number_of_moves < NUMBER_OF_MOVES_OPENING_PHASE:
                opening_move = self.choose_opening_move(arbiter)
                if opening_move[0] != -1:
                    print(f"Best move for opening: {opening_move}")
                    return opening_move
            # First, check immediate rewards or threats
            initial_score = self.score()
            initial_value = self.value()
            max_score_gain = -999999
            max_value_gain = -999999
            for move in self.possible_moves_upper:
                # temporarily change the board to list the possible adversary moves
                i = move[0]
                j = move[1]
                i_new = move[2]
                j_new = move[3]
                piece = self.board[i][j]
                piece_new = self.board[i_new][j_new]
                is_move_a_retreat = self.verify_reverse_moves(i, j, i_new, j_new)
                self.board[i_new][j_new] = self.board[i][j]
                self.board[i][j] = ' '
                self.list_possible_moves(True, self.player)
                new_score = self.score()
                new_value = self.value()
                # returns the board to its previous position
                self.board[i][j] = piece
                self.board[i_new][j_new] = piece_new
                self.list_possible_moves(True, self.player)
                # determine gains
                score_gain = new_score - initial_score
                value_gain = new_value - initial_value
                if is_move_a_retreat == True:
                    score_gain -= RETREAT_PENALTY
                    value_gain -= RETREAT_PENALTY
                if score_gain > max_score_gain:
                    max_score_gain = score_gain
                    best_move_for_score = move
                if value_gain > max_value_gain:
                    max_value_gain = value_gain
                    best_move_for_value = move
            # Here we decide what to do based on the gains (score and value)
            if max_score_gain > SCORE_GAIN_THRESHOLD:
                print(f"Best move for score: {best_move_for_score}")
                return best_move_for_score
            #if max_value_gain > VALUE_GAIN_THRESHOLD:
            else:
                print(f"Best move for value: {best_move_for_value}")
                return best_move_for_value
            """             # If no immediate rewards or threats, then checks if there are intended future moves saved earlier
                        if len(self.intended_future_moves) > 1:
                            print(f"Intended future move: {self.intended_future_moves[0][0]}")
                            next_move = self.intended_future_moves.pop(0)
                            self.intended_future_moves.pop(0)
                            return next_move[0]
                        # If no intended future moves, then check the best move using the minimax algorithm
                        sc = self.minimax(3, -999999, +999999, UPPER, UPPER)
                        print(f"Best move for minimax: {sc[0]}")
                        self.intended_future_moves.extend(sc[2:])
                        return sc[0][0] """
        return [-1, -1, -1, -1]
