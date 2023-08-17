BASE_PIECES = {
    "I1": [(0, 0)],
    "I2": [(0, 0), (1, 0)],
    "I3": [(0, 0), (1, 0), (2, 0)],
    "I4": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "I5": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    "d2": [(0, 0), (1, 1)],
    "d3": [(0, 0), (1, 1), (2, 2)],
    "d4": [(0, 0), (1, 1), (2, 2), (3, 3)],
    "O": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "T": [(0, 1), (1, 0), (1, 1), (1, 2)],
    "TT": [(1, 1), (0, 1), (2, 0), (2, 1), (2, 2)],
    "l": [(0, 0), (1, 0), (1, 1)],
    "L": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "LL": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    "J": [(0, 1), (1, 1), (2, 0), (2, 1)],
    "S": [(0, 1), (0, 2), (1, 0), (1, 1)],
    "Z": [(0, 0), (0, 1), (1, 1), (1, 2)],
    "U": [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)],
    "+": [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
}

def get_piece_size(piece):
    return 1 + max(max([i[0] for i in piece]), max([i[1] for i in piece]))

def print_piece(piece):
    size = get_piece_size(piece)
    little_board = [[0 for _ in range(size)] for _ in range(size)]
    for r, c in piece:
        little_board[r][c] = 1
    for row in little_board:
        print(' '.join(['#' if cell else '.' for cell in row]))

def turn_piece(piece):
    turned = [(-y, x) for (x, y) in piece]
    min_x = min([i[0] for i in turned])
    min_y = min([i[1] for i in turned])
    aligned = [(x - min_x, y - min_y) for (x, y) in turned]
    return aligned

def pieces_are_equal(piece1, piece2):
    return set(piece1) == set(piece2)

def dict_contains_piece(pieces, piece):
    for p in pieces.values():
        if pieces_are_equal(p, piece):
            return True
    return False

def get_pieces():
    pieces = {}
    for label, piece in BASE_PIECES.items():
        pieces[label] = piece
        turned = piece
        for i in range(3):
            turned = turn_piece(turned)
            if not dict_contains_piece(pieces, turned):
                pieces[f"{label}-{i + 1}"] = turned
    return pieces

def get_piece_lines(piece):
    lines = []
    size = get_piece_size(piece)
    little_board = [[0 for _ in range(size)] for _ in range(size)]
    for r, c in piece:
        little_board[r][c] = 1
    for row in little_board:
        lines.append(' '.join(['#' if cell else '.' for cell in row]))
    return lines

def pretty_print(pieces):
    GROUPS = {}
    for label, piece in pieces.items():
        group = label
        if "-" in label:
            group = label.split("-")[0]
        if group not in GROUPS:
            GROUPS[group] = []
        GROUPS[group].append(label)
    print(GROUPS)
    for group, labels in GROUPS.items():
        size = get_piece_size(pieces[labels[0]])
        lines = []
        for _ in range(size + 1):
            lines.append("")
        for label in labels:
            lines[0] += label.ljust(size * 2 + 3)
            piece_lines = get_piece_lines(pieces[label])
            for i in range(size):
                lines[i + 1] += piece_lines[i].ljust(size * 2 + 3)
        for line in lines:
            print(line)
        print()

if __name__ == "__main__":
    pieces = get_pieces()
    pretty_print(pieces)
