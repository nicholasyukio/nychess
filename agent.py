import copy

PLAYER_0 = 0 # Human (or AI under training) (Lower)
PLAYER_1 = 1 # AI (Upper)
LOWER = 0 # Human (or AI under training) (Lower)
UPPER = 1 # AI (Upper)
ARBITER = 2

LOWER_VICTORY = 0
UPPER_VICTORY = 1
GAME_NOT_FINISHED = -1
DRAW = -2
RETREAT_PENALTY = 100

class mind:
    def __init__(self, player):
        self.board = (
        [['R', 'H', 'B', 'Q', 'K', 'B', 'H', 'R'],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
         ['r', 'h', 'b', 'q', 'k', 'b', 'h', 'r']]
         )
        self.reward_matrix = (
        [[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]]
        )
        self.history = []
        self.player = player
        self.adversary = -1
        if player == 1:
            self.adversary = 0
        if player == 0:
            self.adversary = 1
        self.possible_moves_lower = []
        self.possible_moves_upper = []
        self.intended_future_moves = []
        self.points_per_piece = {
        ' ': 0,  # empty space
        'p': 1,  # pawn
        'r': 5,  # rook
        'h': 5,  # horse (knight)
        'b': 5,  # bishop
        'q': 10, # queen
        'k': 100 # king
        }
        self.points_per_siege = 50
        self.points_per_check = 100
        self.points_per_victory = 1000
        self.classic_openings = (
        # Openings that start with e4
        [[[6, 4, 4, 4], [1, 2, 3, 2]], # Sicilian Defense
        [[6, 4, 4, 4], [1, 4, 2, 4]], # French Defense
        [[6, 4, 4, 4], [1, 4, 3, 4], [7, 6, 5, 5], [0, 1, 2, 2], [7, 5, 3, 1]], # Ruy Lopez Openin / Spanish Game / Spanish Opening
        [[6, 4, 4, 4], [1, 2, 2, 2]], # Caro-Kann Defense
        [[6, 4, 4, 4], [1, 4, 3, 4], [7, 6, 5, 5], [0, 1, 2, 2], [7, 5, 4, 2]], # Italian Game
        [[6, 4, 4, 4], [1, 3, 3, 3]], # Scandinavian Defense
        [[6, 4, 4, 4], [1, 3, 2, 3], [6, 3, 4, 3], [0, 6, 2, 5]], # Pirc Defense
        [[6, 4, 4, 4], [0, 6, 2, 5]], # Alekhine Defense
        [[6, 4, 4, 4], [1, 4, 3, 4], [6, 5, 4, 5]], # King's Gambit
        [[6, 4, 4, 4], [1, 4, 3, 4], [7, 6, 5, 5], [0, 1, 2, 2], [6, 3, 4, 3]], # Scotch Game
        [[6, 4, 4, 4], [1, 4, 3, 4], [7, 1, 5, 2]], # Vienna Game
        # Openings that start with d4
        [[6, 3, 4, 3], [1, 3, 3, 3], [6, 2, 4, 2]], # Queen's Gambit
        [[6, 3, 4, 3], [1, 3, 3, 3], [6, 2, 4, 2], [1, 2, 2, 2]], # Slav Defense
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 6, 2, 6]], # King's Indian Defense
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 4, 2, 4], [7, 1, 5, 2], [0, 5, 4, 1]], # Nimzo-Indian Defense
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 4, 2, 4], [7, 6, 5, 5], [1, 1, 2, 1]], # Queen's Indian Defense
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 4, 2, 4], [6, 6, 5, 6]], # Catalan Opening
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 4, 2, 4], [7, 6, 5, 5], [0, 5, 4, 1]], # Bogo-Indian Defense
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 6, 2, 6], [7, 1, 5, 2], [1, 3, 3, 3]], # Grünfeld Defense
        [[6, 3, 4, 3], [1, 5, 3, 5]], # Dutch Defense
        [[6, 3, 4, 3], [0, 6, 2, 5], [7, 2, 3, 6]], # Trompowsky Attack
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 2, 3, 2], [4, 3, 3, 3]], # Benko Gambit
        [[6, 3, 4, 3], [1, 3, 3, 3], [7, 6, 5, 5], [0, 6, 2, 5], [7, 2, 4, 5]], # London System
        [[6, 3, 4, 3], [0, 6, 2, 5], [6, 2, 4, 2], [1, 2, 3, 2], [4, 3, 3, 3], [1, 4, 2, 4], [7, 1, 5, 2], [2, 4, 3, 3], [4, 2, 3, 3], [1, 3, 2, 3]], # Benoni Defense: Modern Variation
        # Other openings
        [[7, 6, 5, 5]], # Reti Opening
        [[6, 2, 4, 2]], # English Opening
        [[6, 5, 4, 5]], # Bird's Opening
        [[7, 6, 5, 5], [1, 3, 3, 3], [6, 6, 5, 6]], # King's Indian Attack
        [[6, 6, 5, 6]], # King's Fianchetto Opening
        [[6, 1, 5, 1]], # Nimzowitsch-Larsen Attack
        [[6, 1, 4, 1]], # Polish Opening
        [[6, 6, 4, 6]]] # Grob Opening
        )
    
    def verify_end_of_game(self):
        self.list_possible_moves(True, UPPER)
        if len(self.possible_moves_upper) == 0:
            if self.verify_check(UPPER):
                #print(f"Checkmate. Player {LOWER} Victory.")
                return LOWER_VICTORY
            else:
                #print(f"Game ended with a draw.")
                return DRAW
        self.list_possible_moves(True, LOWER)
        if len(self.possible_moves_lower) == 0:
            if self.verify_check(LOWER):
                #print(f"Checkmate. Player {UPPER} Victory.")
                return UPPER_VICTORY
            else:
                #print(f"Game ended with a draw.")
                return DRAW
        return GAME_NOT_FINISHED

    def award_points(self, piece, i_new, j_new):
        # Call this method before moving piece
        # Awards points to the entitled player, considering:
        # Check-mate occurence (player wins)
        # Check occurence (adversary king threatened, but not check-mate)
        # Piece captured (pieces to be captured should return positive points in subsequent moves)
        # (pieces lost should return positive points to the adversary and this will be used as parameter in learning process)
        points = 0
        if piece.islower():
            if self.board[i_new][j_new].isupper():
                points += self.points_per_piece[self.board[i_new][j_new].lower()]
                if self.verify_end_of_game() == LOWER_VICTORY:
                    points += self.points_per_victory
                    return points
                else:
                    check = self.verify_check(LOWER)
                    if check > 0:
                        points += check*self.points_per_check
                    return points
        if piece.isupper():
            if self.board[i_new][j_new].islower():
                points += self.points_per_piece[self.board[i_new][j_new].lower()]
                if self.verify_end_of_game() == UPPER_VICTORY:
                    points += self.points_per_victory
                    return points
                else:
                    check = self.verify_check(UPPER)
                    if check > 0:
                        points += check*self.points_per_check
                    return points
        return points

    def neighbours(self, i, j):
        neighbours_list = []
        if i > 0:
            neighbours_list.append([i-1, j])
            if j > 0:
                neighbours_list.append([i-1, j-1])
            if j < 7:
                neighbours_list.append([i-1, j+1]) 
        if i < 7:
            neighbours_list.append([i+1, j])
            if j > 0:
                neighbours_list.append([i+1, j-1])
            if j < 7:
                neighbours_list.append([i+1, j+1]) 
        if j > 0:
            neighbours_list.append([i, j-1])
        if j < 7:
            neighbours_list.append([i, j+1])    
        return neighbours_list

    def is_move_valid(self, i, j, i_new, j_new, verify_check = True):
        if i < 0 or i > 7 or j < 0 or j > 7 or i_new < 0 or i_new > 7 or j_new < 0 or j_new > 7:
            return -1
        if self.board[i][j] == ' ':
            return -1
        if verify_check == True:
            if self.board[i][j].islower() == True and self.verify_check_after_move(i, j, i_new, j_new, LOWER) == True:
                return -3
            if self.board[i][j].isupper() == True and self.verify_check_after_move(i, j, i_new, j_new, UPPER) == True:
                return -3
        # Check for a nearby adversary king
        neighbours_list = self.neighbours(i_new, j_new)
        if self.board[i][j] == 'k': # LOWER king
            for neighbour in neighbours_list:
                if self.board[neighbour[0]][neighbour[1]] == 'K':
                    return -4
        if self.board[i][j] == 'K': # UPPER king
            for neighbour in neighbours_list:
                if self.board[neighbour[0]][neighbour[1]] == 'k':
                    return -4
        # Human piece move
        if self.board[i][j] == 'p':
            if j == j_new:
                if i_new == i - 1 and self.board[i_new][j_new] == ' ':
                    return 1
                if i_new == i - 2 and i == 6 and self.board[i-1][j] == ' ' and self.board[i-2][j] == ' ':
                    return 1
            else:
                if j_new == j - 1 and i_new == i - 1 and self.board[i_new][j_new].isupper() and self.board[i_new][j_new] != ' ':
                    return 1
                if j_new == j + 1 and i_new == i - 1 and self.board[i_new][j_new].isupper() and self.board[i_new][j_new] != ' ':
                    return 1
        if self.board[i][j] == 'r':
            if j == j_new:
                if i_new < i:
                    for k in range(i-1, i_new, -1):
                        if self.board[k][j] != ' ':
                            return -2
                if i_new > i:
                    for k in range(i+1, i_new, +1):
                        if self.board[k][j] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].islower():
                    return -2
                else:
                    return 1
            if i == i_new:
                if j_new < j:
                    for k in range(j-1, j_new, -1):
                        if self.board[i][k] != ' ':
                            return -2
                if j_new > j:
                    for k in range(j+1, j_new, +1):
                        if self.board[i][k] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].islower():
                    return -2
                else:
                    return 1
        if self.board[i][j] == 'h':
            if abs(i-i_new)*abs(j-j_new) == 2:
                if self.board[i_new][j_new] == ' ' or self.board[i_new][j_new].isupper():
                    return 1
                else:
                    return -2
            else:
                return -2
        if self.board[i][j] == 'b':
            if abs(i-i_new) == abs(j-j_new):
                if self.board[i_new][j_new].isupper() or self.board[i_new][j_new] == ' ':
                    if i_new > i and j_new > j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                    if i_new > i and j_new < j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new > j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new < j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                else:
                    return -2
            else:
                return -2
        if self.board[i][j] == 'q':
            # Rook like movements
            if j == j_new:
                if i_new < i:
                    for k in range(i-1, i_new, -1):
                        if self.board[k][j] != ' ':
                            return -2
                if i_new > i:
                    for k in range(i+1, i_new, +1):
                        if self.board[k][j] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].islower():
                    return -2
                else:
                    return 1
            if i == i_new:
                if j_new < j:
                    for k in range(j-1, j_new, -1):
                        if self.board[i][k] != ' ':
                            return -2
                if j_new > j:
                    for k in range(j+1, j_new, +1):
                        if self.board[i][k] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].islower():
                    return -2
                else:
                    return 1
            # Bishop like movements
            if abs(i-i_new) == abs(j-j_new):
                if self.board[i_new][j_new].isupper() or self.board[i_new][j_new] == ' ':
                    if i_new > i and j_new > j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                    if i_new > i and j_new < j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new > j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new < j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                else:
                    return -2
            else:
                return -2
        if self.board[i][j] == 'k':
            if abs(i-i_new) < 2 and abs(j-j_new) < 2:
                if self.board[i_new][j_new] == ' ' or self.board[i_new][j_new].isupper() == True:
                    return 1
                    # check threat
                    """ if self.verify_check_in_me(i_new, j_new) == False:
                        return 1
                    else:
                        return -3 """
                else:
                    return -2
            else:
                return -2
        # AI piece move
        if self.board[i][j] == 'P':
            if j == j_new:
                if i_new == i + 1 and self.board[i_new][j_new] == ' ':
                    return 1
                if i_new == i + 2 and i == 1 and self.board[i+1][j] == ' ' and self.board[i+2][j] == ' ':
                    return 1
            else:
                if j_new == j - 1 and i_new == i + 1 and self.board[i_new][j_new].islower() and self.board[i_new][j_new] != ' ':
                    return 1
                if j_new == j + 1 and i_new == i + 1 and self.board[i_new][j_new].islower() and self.board[i_new][j_new] != ' ':
                    return 1
        if self.board[i][j] == 'R':
            if j == j_new:
                if i_new < i:
                    for k in range(i-1, i_new, -1):
                        if self.board[k][j] != ' ':
                            return -2
                if i_new > i:
                    for k in range(i+1, i_new, +1):
                        if self.board[k][j] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].isupper():
                    return -2
                else:
                    return 1
            if i == i_new:
                if j_new < j:
                    for k in range(j-1, j_new, -1):
                        if self.board[i][k] != ' ':
                            return -2
                if j_new > j:
                    for k in range(j+1, j_new, +1):
                        if self.board[i][k] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].isupper():
                    return -2
                else:
                    return 1
        if self.board[i][j] == 'H':
            if abs(i-i_new)*abs(j-j_new) == 2:
                if self.board[i_new][j_new] == ' ' or self.board[i_new][j_new].islower():
                    return 1
                else:
                    return -2
            else:
                return -2
        if self.board[i][j] == 'B':
            if abs(i-i_new) == abs(j-j_new):
                if self.board[i_new][j_new].islower() or self.board[i_new][j_new] == ' ':
                    if i_new > i and j_new > j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                    if i_new > i and j_new < j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new > j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new < j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                else:
                    return -2
            else:
                return -2
        if self.board[i][j] == 'Q':
            # Rook like movements
            if j == j_new:
                if i_new < i:
                    for k in range(i-1, i_new, -1):
                        if self.board[k][j] != ' ':
                            return -2
                if i_new > i:
                    for k in range(i+1, i_new, +1):
                        if self.board[k][j] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].isupper():
                    return -2
                else:
                    return 1
            if i == i_new:
                if j_new < j:
                    for k in range(j-1, j_new, -1):
                        if self.board[i][k] != ' ':
                            return -2
                if j_new > j:
                    for k in range(j+1, j_new, +1):
                        if self.board[i][k] != ' ':
                            return -2
                if self.board[i_new][j_new] != ' ' and self.board[i_new][j_new].isupper():
                    return -2
                else:
                    return 1
            # Bishop like movements
            if abs(i-i_new) == abs(j-j_new):
                if self.board[i_new][j_new].islower() or self.board[i_new][j_new] == ' ':
                    if i_new > i and j_new > j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                    if i_new > i and j_new < j:
                        for k in range(i+1, i_new, +1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new > j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j-k+i] != ' ':
                                return -2
                        return 1
                    if i_new < i and j_new < j:
                        for k in range(i-1, i_new, -1):
                            if self.board[k][j+k-i] != ' ':
                                return -2
                        return 1
                else:
                    return -2
            else:
                return -2
        if self.board[i][j] == 'K':
            if abs(i-i_new) < 2 and abs(j-j_new) < 2:
                if self.board[i_new][j_new] == ' ' or self.board[i_new][j_new].islower() == True:
                    return 1
                    # check threat
                    """ if self.verify_check_in_me(i_new, j_new) == False:
                        return 1
                    else:
                        return -3 """
                else:
                    return -2
            else:
                return -2

    def find_king(self, player):
        i_king = -1
        j_king = -1
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'k' and player == LOWER:
                    i_king = i
                    j_king = j
                if self.board[i][j] == 'K' and player == UPPER:
                    i_king = i
                    j_king = j
        return i_king, j_king
    
    def verify_check(self, player):
        check = 0
        i_king, j_king = self.find_king(player)
        #print(f"King position for player {player}: {i_king}, {j_king}")
        if player == LOWER:
            self.list_possible_moves(False, UPPER)
            for move in self.possible_moves_upper:
                #print(f"Analyzing check for move: {move}")
                if move[2] == i_king and move[3] == j_king:
                    #print("Check threat!")
                    check += 1 # this returns the number of pieces checking the king
            self.list_possible_moves(False, UPPER)
        if player == UPPER:
            self.list_possible_moves(False, LOWER)
            for move in self.possible_moves_lower:
                #print(f"Analyzing check for move: {move}")
                if move[2] == i_king and move[3] == j_king:
                    #print("Check threat!")
                    check += 1 # this returns the number of pieces checking the king
            self.list_possible_moves(False, LOWER)
        return check
    
    def verify_check_after_move(self, i, j, i_new, j_new, player):
        # temporarily change the board to list the possible adversary moves
        piece = self.board[i][j]
        piece_new = self.board[i_new][j_new]
        self.board[i_new][j_new] = self.board[i][j]
        self.board[i][j] = ' '
        if self.verify_check(player) == 0:
            check = False
        else:
            check = True
        # returns the board to its previous position
        self.board[i][j] = piece
        self.board[i_new][j_new] = piece_new
        #print("Check after move: ", check)
        return check
    
    def find_own_king(self):
        i_king = -1
        j_king = -1
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'k' and self.player == PLAYER_0:
                    i_king = i
                    j_king = j
                if self.board[i][j] == 'K' and self.player == PLAYER_1:
                    i_king = i
                    j_king = j
        return i_king, j_king
    
    def list_possible_moves(self, verify_check, player = ARBITER):
        if player == LOWER or player == ARBITER:
            self.possible_moves_lower.clear()
        if player == UPPER or player == ARBITER:
            self.possible_moves_upper.clear()
        for i in range(8):
            for j in range(8):
                # PLAYER 1 (UPPER)
                if player == UPPER or player == ARBITER:
                    if self.board[i][j] == 'P':
                        if self.is_move_valid(i, j, i+1, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j])
                        if self.is_move_valid(i, j, i+2, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+2, j])
                        if self.is_move_valid(i, j, i+1, j+1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j+1])
                        if self.is_move_valid(i, j, i+1, j-1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j-1])
                    if self.board[i][j] == 'R':
                        k = 1
                        while self.is_move_valid(i, j, i+k, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j+k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j-k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i, j-k])
                            k += 1
                    if self.board[i][j] == 'H':
                        if self.is_move_valid(i, j, i+1, j+2, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j+2])
                        if self.is_move_valid(i, j, i+1, j-2, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j-2])
                        if self.is_move_valid(i, j, i-1, j+2, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-1, j+2])
                        if self.is_move_valid(i, j, i-1, j-2, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-1, j-2])
                        if self.is_move_valid(i, j, i+2, j+1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+2, j+1])
                        if self.is_move_valid(i, j, i+2, j-1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+2, j-1])
                        if self.is_move_valid(i, j, i-2, j+1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-2, j+1])
                        if self.is_move_valid(i, j, i-2, j-1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-2, j-1])
                    if self.board[i][j] == 'B':
                        k = 1
                        while self.is_move_valid(i, j, i+k, j+k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j+k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i+k, j-k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+k, j-k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j-k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-k, j-k])
                            k += 1
                    if self.board[i][j] == 'Q':
                        # Rook like movements
                        k = 1
                        while self.is_move_valid(i, j, i+k, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j+k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j-k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i, j-k])
                            k += 1
                        # Bishop like movements
                        k = 1
                        while self.is_move_valid(i, j, i+k, j+k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j+k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i+k, j-k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+k, j-k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j-k, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-k, j-k])
                            k += 1
                    if self.board[i][j] == 'K':
                        if self.is_move_valid(i, j, i+1, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j])
                        if self.is_move_valid(i, j, i+1, j-1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j-1])
                        if self.is_move_valid(i, j, i+1, j+1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i+1, j+1])
                        if self.is_move_valid(i, j, i, j+1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i, j+1])
                        if self.is_move_valid(i, j, i, j-1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i, j-1])
                        if self.is_move_valid(i, j, i-1, j, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-1, j])
                        if self.is_move_valid(i, j, i-1, j-1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-1, j-1])
                        if self.is_move_valid(i, j, i-1, j+1, verify_check) == 1:
                            self.possible_moves_upper.append([i, j, i-1, j+1])
                if player == LOWER or player == ARBITER:
                    # PLAYER 0 (LOWER)
                    if self.board[i][j] == 'p':
                        if self.is_move_valid(i, j, i-1, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j])
                        if self.is_move_valid(i, j, i-2, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-2, j])
                        if self.is_move_valid(i, j, i-1, j+1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j+1])
                        if self.is_move_valid(i, j, i-1, j-1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j-1])
                    if self.board[i][j] == 'r':
                        k = 1
                        while self.is_move_valid(i, j, i+k, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j+k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j-k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i, j-k])
                            k += 1
                    if self.board[i][j] == 'h':
                        if self.is_move_valid(i, j, i+1, j+2, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+1, j+2])
                        if self.is_move_valid(i, j, i+1, j-2, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+1, j-2])
                        if self.is_move_valid(i, j, i-1, j+2, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j+2])
                        if self.is_move_valid(i, j, i-1, j-2, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j-2])
                        if self.is_move_valid(i, j, i+2, j+1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+2, j+1])
                        if self.is_move_valid(i, j, i+2, j-1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+2, j-1])
                        if self.is_move_valid(i, j, i-2, j+1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-2, j+1])
                        if self.is_move_valid(i, j, i-2, j-1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-2, j-1])
                    if self.board[i][j] == 'b':
                        k = 1
                        while self.is_move_valid(i, j, i+k, j+k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j+k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i+k, j-k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+k, j-k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j-k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-k, j-k])
                            k += 1
                    if self.board[i][j] == 'q':
                        # Rook like movements
                        k = 1
                        while self.is_move_valid(i, j, i+k, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-k, j])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j+k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i, j-k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i, j-k])
                            k += 1
                        # Bishop like movements
                        k = 1
                        while self.is_move_valid(i, j, i+k, j+k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j+k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-k, j+k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i+k, j-k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+k, j-k])
                            k += 1
                        k = 1
                        while self.is_move_valid(i, j, i-k, j-k, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-k, j-k])
                            k += 1
                    if self.board[i][j] == 'k':
                        if self.is_move_valid(i, j, i+1, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+1, j])
                        if self.is_move_valid(i, j, i+1, j-1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+1, j-1])
                        if self.is_move_valid(i, j, i+1, j+1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i+1, j+1])
                        if self.is_move_valid(i, j, i, j+1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i, j+1])
                        if self.is_move_valid(i, j, i, j-1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i, j-1])
                        if self.is_move_valid(i, j, i-1, j, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j])
                        if self.is_move_valid(i, j, i-1, j-1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j-1])
                        if self.is_move_valid(i, j, i-1, j+1, verify_check) == 1:
                            self.possible_moves_lower.append([i, j, i-1, j+1])

    def print_possible_moves(self):
        print("Possible moves (LOWER):")
        print(self.possible_moves_lower)
        print("Possible moves (UPPER):")
        print(self.possible_moves_upper)

    def value(self):
        value = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j].islower():
                    value = value - self.points_per_piece[self.board[i][j].lower()]
                if self.board[i][j].isupper():
                    value = value + self.points_per_piece[self.board[i][j].lower()]
        return value

    def score(self):
        # Calculates the points of the LOWER player
        self.list_possible_moves(True, LOWER)
        points_lower = 0
        for move in self.possible_moves_lower:
            i = move[0]
            j = move[1]
            i_new = move[2]
            j_new = move[3]
            points_lower += self.award_points(self.board[i][j], i_new, j_new)
            # Additional points in case of sieging adversary king
            i_adv_king, j_adv_king = self.find_king(UPPER)
            dist_king_i = i_new - i_adv_king
            dist_king_j = j_new - j_adv_king
            if abs(dist_king_i) <= 1 and abs(dist_king_j) <= 1 and abs(dist_king_i)+abs(dist_king_j) > 0: 
                points_lower += self.points_per_siege
        # Calculates the points of the UPPER player
        self.list_possible_moves(True, UPPER)
        points_upper = 0
        for move in self.possible_moves_upper:
            i = move[0]
            j = move[1]
            i_new = move[2]
            j_new = move[3]
            points_upper += self.award_points(self.board[i][j], i_new, j_new)
            # Additional points in case of sieging adversary king
            i_adv_king, j_adv_king = self.find_king(LOWER)
            dist_king_i = i_new - i_adv_king
            dist_king_j = j_new - j_adv_king
            if abs(dist_king_i) <= 1 and abs(dist_king_j) <= 1 and abs(dist_king_i)+abs(dist_king_j) > 0: 
                points_upper += self.points_per_siege
        # Calculates and returns the difference (UPPER-LOWER)
        return points_upper - points_lower
    
    def verify_reverse_moves(self, i, j, i_new, j_new):
        for move_reg in self.history:
            board = move_reg[0]
            move = [move_reg[1], move_reg[2], move_reg[3], move_reg[4]]
            piece = board[move[0]][move[1]]
            if move[0] == i_new and move[1] == j_new and move[2] == i and move[3] == j and piece == self.board[i][j]:
                return True
        return False
    
    def minimax(self, depth, alpha, beta, player, acting_player):
        N = 2  # Number of moves analyzed of the acting player
        M = 1 # Number of moves analyzed of the opponent player
        def determine_score_gain(move):
            self.list_possible_moves(True, self.player)
            # temporarily change the board to list the possible adversary moves
            initial_score = self.score()
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
            # determine gains
            score_gain = new_score - initial_score
            if is_move_a_retreat == True:
                score_gain -= RETREAT_PENALTY
            # returns the board to its previous position
            self.board[i][j] = piece
            self.board[i_new][j_new] = piece_new
            self.list_possible_moves(True, self.player)
            return score_gain
        return_list = []
        #print(f"depth: {depth}")
        #self.print_board()
        if player == LOWER:
            if acting_player == LOWER:
                self.list_possible_moves(True, LOWER)
                if depth == 0 or len(self.possible_moves_lower) == 0:
                    return [[[0, 0, 0, 0], self.score()]]
                minEval = +999999
                possible_moves = copy.copy(self.possible_moves_lower)
                possible_moves = sorted(possible_moves, key=determine_score_gain, reverse=False)
                selected_moves = possible_moves[:N]
                #for move in possible_moves:
                for move in selected_moves:
                    piece_initial = self.board[move[0]][move[1]]
                    piece_final = self.board[move[2]][move[3]]
                    self.board[move[2]][move[3]] = piece_initial
                    self.board[move[0]][move[1]] = ' '
                    return_child = self.minimax(depth-1, alpha, beta, UPPER, acting_player)
                    #print(f"Return child: {return_child}")
                    eval = return_child[-1][1]
                    # Return the board to its previous position
                    self.board[move[0]][move[1]] = piece_initial
                    self.board[move[2]][move[3]] = piece_final
                    if eval < minEval:
                        minEval = eval
                        best_move = move
                        best_child = return_child
                    if eval < beta:
                        beta = eval
                    if beta <= alpha:
                        break
                return_list.append([best_move, minEval])
                return_list.extend(best_child)
                return return_list
            if acting_player == UPPER:
                self.list_possible_moves(True, LOWER)
                if depth == 0 or len(self.possible_moves_lower) == 0:
                    return [[[0, 0, 0, 0], self.score()]]
                possible_moves = copy.copy(self.possible_moves_lower)
                possible_moves = sorted(possible_moves, key=determine_score_gain, reverse=False)
                selected_moves = possible_moves[:M]
                max_points = -999999
                best_move = []
                #for move in possible_moves:
                for move in selected_moves:
                    points = self.award_points(self.board[move[0]][move[1]], move[2], move[3])
                    if points > max_points:
                        max_points = points
                        best_move = copy.copy(move)
                piece_initial = self.board[best_move[0]][best_move[1]]
                piece_final = self.board[best_move[2]][best_move[3]]
                self.board[best_move[2]][best_move[3]] = piece_initial
                self.board[best_move[0]][best_move[1]] = ' '
                return_child = self.minimax(depth-1, alpha, beta, UPPER, acting_player)
                #print(f"Return child: {return_child}")
                eval = return_child[-1][1]
                # Return the board to its previous position
                self.board[best_move[0]][best_move[1]] = piece_initial
                self.board[best_move[2]][best_move[3]] = piece_final
                return_list.append([best_move, eval])
                return_list.extend(return_child)
                return return_list
        if player == UPPER:
            if acting_player == UPPER:
                self.list_possible_moves(True, UPPER)
                if depth == 0 or len(self.possible_moves_upper) == 0:
                    return [[[0, 0, 0, 0], self.score()]]
                maxEval = -999999
                possible_moves = copy.copy(self.possible_moves_upper)
                possible_moves = sorted(possible_moves, key=determine_score_gain, reverse=True)
                selected_moves = possible_moves[:N]
                #for move in possible_moves:
                for move in selected_moves:
                    piece_initial = self.board[move[0]][move[1]]
                    piece_final = self.board[move[2]][move[3]]
                    self.board[move[2]][move[3]] = piece_initial
                    self.board[move[0]][move[1]] = ' '
                    return_child = self.minimax(depth-1, alpha, beta, LOWER, acting_player)
                    #print(f"Return child: {return_child}")
                    eval = return_child[-1][1]
                    # Return the board to its previous position
                    self.board[move[0]][move[1]] = piece_initial
                    self.board[move[2]][move[3]] = piece_final
                    if eval > maxEval:
                        maxEval = eval
                        best_move = move
                        best_child = return_child
                    if eval > alpha:
                        alpha = eval
                    if beta <= alpha:
                        break
                return_list.append([best_move, maxEval])
                return_list.extend(best_child)
                return return_list
            if acting_player == LOWER:
                self.list_possible_moves(True, UPPER)
                if depth == 0 or len(self.possible_moves_upper) == 0:
                    return [[[0, 0, 0, 0], self.score()]]
                possible_moves = copy.copy(self.possible_moves_upper)
                possible_moves = sorted(possible_moves, key=determine_score_gain, reverse=True)
                selected_moves = possible_moves[:M]
                max_points = -999999
                best_move = []
                #for move in possible_moves:
                for move in selected_moves:
                    points = self.award_points(self.board[move[0]][move[1]], move[2], move[3])
                    if points > max_points:
                        max_points = points
                        best_move = copy.copy(move)
                piece_initial = self.board[best_move[0]][best_move[1]]
                piece_final = self.board[best_move[2]][best_move[3]]
                self.board[best_move[2]][best_move[3]] = piece_initial
                self.board[best_move[0]][best_move[1]] = ' '
                return_child = self.minimax(depth-1, alpha, beta, LOWER, acting_player)
                #print(f"Return child: {return_child}")
                eval = return_child[-1][1]
                # Return the board to its previous position
                self.board[best_move[0]][best_move[1]] = piece_initial
                self.board[best_move[2]][best_move[3]] = piece_final
                return_list.append([best_move, eval])
                return_list.extend(return_child)
                return return_list
        
    def print_board(self):
        # prints the reference board
        i = 0
        j = 0
        print("Current chess board:")
        print("  ", end='')
        for i in range(len(self.board)):
            print("| ", end='')
            print(i, end=' ')
        print("|\n")
        for i in range(len(self.board)):
            print(i, end=' ')
            print("| ", end='')
            for j in range(len(self.board[i])):
                print(self.board[i][j], end=' | ')
            print("\n")
        print(f"Current board score: {self.score()}")