import random
from board import Board
from piece import get_pieces, print_piece

# Testing the WoodokuBoard class
board = Board()
# print("Initial Board:")
# board.print_board()

board_str = """# . . . # . # # .
. # . . . . # . .
. # # . . . # . .
. # # . # # . . .
. . . . . . . . .
. # # . # . . . #
. . # # . # # . .
# . # . # # # # .
. . . . . . . . ."""
board.set_str(board_str)
board.print_board()

# Game loop
PIECES = get_pieces()
for iteration in range(1000):
    print(f"\n\n----- Iteration {iteration}")

    pieces_to_test = []
    for _ in range(3):
        piece_str = ""
        while piece_str not in PIECES:
            piece_str = input("Please input a piece: ")
            if piece_str not in PIECES:
                print(f"{piece_str} is not a valid piece label.")
        piece = PIECES[piece_str]
        print("You chose this piece:")
        print_piece(piece)
        pieces_to_test.append(piece)
    print("\nCalculating best moves...")
    while pieces_to_test and not board.is_game_over(pieces_to_test):
        best_piece, best_move, best_score = board.best_move_with_lookahead(pieces_to_test)
        # print("\nPieces:")
        # for piece in pieces_to_test:
        #     print()
        #     print_piece(piece)
        # print("\nBest piece to start with:", best_piece)
        # print("Best move for this piece:", best_move)
        board.apply_move(best_move)
        print("\nBoard after applying best move:")
        board.print_board()
        pieces_to_test.remove(best_piece)
    if pieces_to_test and board.is_game_over(pieces_to_test):
        break

if len(pieces_to_test) > 0 and board.is_game_over(pieces_to_test):
    print("Game over.")
