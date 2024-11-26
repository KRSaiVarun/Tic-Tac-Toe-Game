def print_board(board):
    """Prints the current state of the board without displaying numbers for empty spaces."""
    print("Current Board:")
    for row in board:
        print(" | ".join(cell if cell != ' ' else ' ' for cell in row))
        print("-" * 5)


def check_winner(board):
    """Checks if there's a winner."""
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
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


def tic_tac_toe():
    """Main function to play the Tic-tac-toe game."""
    print("Welcome to Tic-Tac-Toe!")
    player1 = input("Enter name for Player 1 (X): ")
    player2 = input("Enter name for Player 2 (O): ")
    players = [player1, player2]
    symbols = ['X', 'O']

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


if __name__ == "__main__":
    tic_tac_toe()
