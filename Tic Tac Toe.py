import sys
from random import choice

# Constants for players
PLAYER_X = 'X'  # Human plays as X
PLAYER_O = 'O'  # AI or second player plays as O

def print_board(board):
    """Prints the game board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    """Check if there's a winner."""
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  # rows
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  # columns
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  # diagonals
    ]
    for condition in win_conditions:
        values = [board[x][y] for x, y in condition]
        if values[0] != ' ' and all(v == values[0] for v in values):
            return values[0]
    return None

def is_board_full(board):
    """Checks if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def get_move(player):
    """Prompts the player to enter a valid move."""
    while True:
        try:
            move = int(input(f"{player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                raise ValueError("Invalid move. Must be between 1 and 9.")
            return move
        except ValueError as e:
            print(e)

def make_move(board, move, player):
    """Places the player's move on the board."""
    row, col = divmod(move, 3)
    if board[row][col] == ' ':
        board[row][col] = player
        return True
    else:
        print("That spot is already taken. Try again.")
        return False

def reset_board():
    """Resets the game board."""
    return [[' ' for _ in range(3)] for _ in range(3)]

def get_empty_cells(board):
    """Returns a list of available (row, col) positions."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def medium_strategy(board):
    """Checks if the AI can win or block the opponent."""
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = PLAYER_O  # Simulate computer move
                if check_winner(board) == PLAYER_O:
                    return i, j  # Block or win
                board[i][j] = ' '  # Undo move

                board[i][j] = PLAYER_X  # Simulate player move
                if check_winner(board) == PLAYER_X:
                    return i, j  # Block player
                board[i][j] = ' '  # Undo move
    return None  # No winning or blocking move found

def minimax(board, is_maximizing, depth):
    """Minimax algorithm for decision making."""
    winner = check_winner(board)
    if winner == PLAYER_X:
        return -10 + depth
    if winner == PLAYER_O:
        return 10 - depth
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = PLAYER_O
            score = minimax(board, False, depth + 1)
            board[i][j] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = PLAYER_X
            score = minimax(board, True, depth + 1)
            board[i][j] = ' '
            best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    """Finds the best move for the AI using Minimax."""
    best_move = None
    best_score = -float('inf')
    for i, j in get_empty_cells(board):
        board[i][j] = PLAYER_O
        score = minimax(board, False, 0)
        board[i][j] = ' '
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

def computer_turn(board, difficulty):
    """Handle the computer's turn based on difficulty."""
    print("Computer's turn (O). Thinking...")
    if difficulty == "Easy":
        x, y = choice(get_empty_cells(board))
    elif difficulty == "Medium":
        move = medium_strategy(board)
        if move is None:
            x, y = choice(get_empty_cells(board))  # Random move
        else:
            x, y = move
    elif difficulty == "Hard":
        x, y = get_best_move(board)
    else:
        x, y = choice(get_empty_cells(board))  # Default random
    print(f"Computer Move: O in {x * 3 + y + 1}")
    board[x][y] = PLAYER_O
    print_board(board)

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

def play_human_vs_human():
    """Function for Human vs. Human mode."""
    print("Human vs. Human Mode")
    player1 = input("Enter name for Player 1 (X): ")
    player2 = input("Enter name for Player 2 (O): ")
    players = [player1, player2]
    symbols = [PLAYER_X, PLAYER_O]

    while True:
        board = reset_board()
        current_player = 0

        while True:
            print_board(board)
            print(f"{players[current_player]}'s turn ({symbols[current_player]})")
            move = get_move(players[current_player])

            if make_move(board, move, symbols[current_player]):
                winner = check_winner(board)
                if winner:
                    print_board(board)
                    print(f"{players[current_player]} wins!")
                    break
                if is_board_full(board):
                    print_board(board)
                    print("It's a tie!")
                    break
                current_player = 1 - current_player  # Switch players

        if input("Do you want to play again? (y/n): ").lower() != 'y':
            print("Thanks for playing!")
            break

def play_human_vs_computer():
    """Function for Human vs. AI mode."""
    print("Human vs. Computer Mode")
    player_name = input("Enter your name: ")
    difficulty = choose_difficulty()

    while True:
        board = reset_board()
        print_board(board)

        while True:
            move = get_move(player_name)
            if make_move(board, move, PLAYER_X):
                winner = check_winner(board)
                if winner:
                    print_board(board)
                    print(f"{player_name} wins!")
                    break
                if is_board_full(board):
                    print_board(board)
                    print("It's a tie!")
                    break

                computer_turn(board, difficulty)
                winner = check_winner(board)
                if winner:
                    print_board(board)
                    print("The computer wins!")
                    break
                if is_board_full(board):
                    print_board(board)
                    print("It's a tie!")
                    break

        if input("Do you want to play again? (y/n): ").lower() != 'y':
            print("Thanks for playing!")
            break

def main_menu():
    """Displays the main menu and allows the user to choose a game mode."""
    while True:
        print("Welcome to Tic-Tac-Toe!")
        print("Select Game Mode:")
        print("1. Human vs. Human")
        print("2. Human vs. Computer")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            play_human_vs_human()
        elif choice == '2':
            play_human_vs_computer()
        elif choice == '3':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
