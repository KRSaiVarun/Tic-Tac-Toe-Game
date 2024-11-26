import sys
from random import choice

# Constants
PLAYER = 1  # Human plays as X
COMPUTER = 0  # Computer plays as O

def print_board(board):
    """Prints the game board."""
    symbols = {1: 'X', 0: 'O', -1: ' '}
    for row in board:
        print(" | ".join(symbols[cell] for cell in row))
        print("-" * 9)

def check_win(board):
    """Check if there's a winner."""
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  # rows
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  # columns
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  # diagonals
    ]
    for condition in win_conditions:
        values = [board[x][y] for x, y in condition]
        if values[0] != -1 and all(v == values[0] for v in values):
            return True
    return False

def check_tie(board):
    """Check for a tie."""
    return all(cell != -1 for row in board for cell in row)

def get_player_input():
    """Get player input and validate."""
    while True:
        try:
            move = int(input("Your turn (X), choose a cell (1-9): "))
            if move in range(1, 10):
                return divmod(move - 1, 3)
            else:
                print("Move must be between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def player_turn(board):
    """Handle the player's turn."""
    while True:
        x, y = get_player_input()
        if board[x][y] == -1:
            board[x][y] = PLAYER
            break
        else:
            print("Cell already taken. Try again.")

def computer_turn(board, difficulty):
    """Handle the computer's turn based on difficulty."""
    print("Computer's turn (O). Thinking...")
    if difficulty == "Easy":
        x, y = choice(get_empty_cells(board))
        print(f"Computer Move (Random): O in {x * 3 + y + 1}")
    elif difficulty == "Medium":
        move = medium_strategy(board)
        if move is not None:
            x, y = move
            print(f"Computer Move (Block/Wins): O in {x * 3 + y + 1}")
        else:
            x, y = choice(get_empty_cells(board))
            print(f"Computer Move (Random): O in {x * 3 + y + 1}")
    elif difficulty == "Hard":
        move = minimax(board, COMPUTER)
        x, y = move[0], move[1]
        print(f"Computer Move (Strategic): O in {x * 3 + y + 1}")
    else:
         x, y = choice(get_empty_cells(board))
         print(f"Computer Move (Random): O in {x * 3 + y + 1}")

    board[x][y] = COMPUTER
    print_board(board)

def get_empty_cells(board):
    """Get a list of empty cells."""
    return [(x, y) for x in range(3) for y in range(3) if board[x][y] == -1]

def medium_strategy(board):
    """Basic strategy for medium difficulty."""
    for x, y in get_empty_cells(board):
        board[x][y] = COMPUTER
        if check_win(board):
            board[x][y] = -1  # Reset cell
            return x, y  # Win if possible
        board[x][y] = -1  # Reset cell
    
    for x, y in get_empty_cells(board):
        board[x][y] = PLAYER
        if check_win(board):
            board[x][y] = -1  # Reset cell
            return x, y  # Block if necessary
        board[x][y] = -1  # Reset cell

    return None  # No immediate strategy found

def minimax(board, player):
    """Minimax algorithm for AI."""
    if check_win(board):
        return [None, None, 1 if player == COMPUTER else -1]
    elif check_tie(board):
        return [None, None, 0]

    best = [None, None, -float('inf')] if player == COMPUTER else [None, None, float('inf')]

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == -1:
                board[x][y] = player
                score = minimax(board, -player)
                board[x][y] = -1
                score[0], score[1] = x, y

                if player == COMPUTER:
                    if score[2] > best[2]:
                        best = score
                else:
                    if score[2] < best[2]:
                        best = score
    return best

def choose_difficulty():
    """Let the player choose a difficulty level."""
    print("Choose a difficulty level:")
    print("1. Easy (Random Moves)")
    print("2. Medium (Basic Strategy)")
    print("3. Hard (Advanced Strategy)")
    while True:
        choice = input("Enter the number of your choice: ")
        if choice in ["1", "2", "3"]:
            return ["Easy", "Medium", "Hard"][int(choice) - 1]
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def start_game():
    """Initialize and start the game."""
    board = [[-1 for _ in range(3)] for _ in range(3)]
    difficulty = choose_difficulty()
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    while not check_win(board) and not check_tie(board):
        player_turn(board)
        print_board(board)
        if check_win(board):
            print("Congratulations, you won!")
            break
        if check_tie(board):
            print("It's a tie!")
            break
        computer_turn(board, difficulty)
        if check_win(board):
            print("The computer wins!")
            break

    if input("Play again? (y/n): ").lower() == 'y':
        start_game()

if __name__ == "__main__":
    start_game()
