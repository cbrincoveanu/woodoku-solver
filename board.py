class Board:
    def __init__(self):
        self.board = self.create_empty_board()
        self.score = 0
        self.previous_states = []  # To store previous board states
        self.previous_moves = []  # To store previous moves
        self.previous_scores = []  # To store previous scores

    def set_str(self, board_str):
        rows = board_str.split("\n")
        for r, row in enumerate(rows):
            cells = row.split(" ")
            for c, cell in enumerate(cells):
                self.board[r][c] = 1 if cell == '#' else 0
    
    def create_empty_board(self):
        return [[0 for _ in range(9)] for _ in range(9)]

    def valid_moves(self, piece):
        moves = []
        max_row = 9 - max([p[0] for p in piece])
        max_col = 9 - max([p[1] for p in piece])

        for r in range(max_row):
            for c in range(max_col):
                if all(self.board[r + p[0]][c + p[1]] == 0 for p in piece):
                    moves.append([(r + p[0], c + p[1]) for p in piece])

        return moves

    def apply_move(self, move):
        # Save the current state and move before applying the new move
        self.previous_states.append([row.copy() for row in self.board])
        self.previous_moves.append(move.copy())
        self.previous_scores.append(self.score)

        # Apply the move
        for r, c in move:
            self.board[r][c] = 1
            self.score += 1
        
        # Mark cells to be emptied
        to_empty = set()

        # Check rows
        for r in range(9):
            if sum(self.board[r]) == 9:
                self.score += 18
                for c in range(9):
                    to_empty.add((r, c))

        # Check columns
        for c in range(9):
            if sum([self.board[r][c] for r in range(9)]) == 9:
                self.score += 18
                for r in range(9):
                    to_empty.add((r, c))

        # Check 3x3 blocks
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                if sum([self.board[r + i][c + j] for i in range(3) for j in range(3)]) == 9:
                    self.score += 18
                    for i in range(3):
                        for j in range(3):
                            to_empty.add((r + i, c + j))

        # Empty the marked cells
        for r, c in to_empty:
            self.board[r][c] = 0

    def undo(self):
        if not self.previous_states:
            print("Cannot undo: At the initial state.")
            return

        # Revert to the previous state and move
        self.board = self.previous_states.pop()
        self.previous_moves.pop()
        self.score = self.previous_scores.pop()

    def evaluate_board(self):
        # Count the number of empty squares on the board
        return self.score # sum([1 for row in self.board for cell in row if cell == 0])

    def is_game_over(self, pieces):
        return all([len(self.valid_moves(piece)) == 0 for piece in pieces])

    def best_move_with_lookahead(self, pieces, depth=2):
        best_score = float('-inf')
        best_piece = None
        best_move_for_piece = None

        # For each given piece and its orientation
        for piece in pieces:
            # Get all valid moves for this piece
            moves = self.valid_moves(piece)
            
            for move in moves:
                # Simulate applying the move
                self.apply_move(move)

                # If there are other pieces left and depth is not exhausted, continue the lookahead
                next_pieces = pieces.copy()
                next_pieces.remove(piece)

                if depth > 0 and next_pieces:
                    _, _, score = self.best_move_with_lookahead(next_pieces, depth - 1)
                else:
                    score = self.evaluate_board()

                # Revert the move to continue the search
                self.undo()

                if score >= best_score:
                    best_score = score
                    best_piece = piece
                    best_move_for_piece = move

        return best_piece, best_move_for_piece, best_score

    def get_char(self, cell):
        return 'X' if cell == 2 else ('#' if cell == 1 else '.')

    def print_board(self, show_last_move=True):
        tmp_board = self.create_empty_board()
        for r in range(9):
            for c in range(9):
                tmp_board[r][c] = self.board[r][c]
        
        if show_last_move and len(self.previous_moves) > 0:
            move = self.previous_moves[-1]
            for r, c in move:
                tmp_board[r][c] = 2
        for row in tmp_board:
            print(' '.join([self.get_char(cell) for cell in row]))
        print(f"Score: {self.score}")
