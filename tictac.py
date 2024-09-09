import random
import math

# Initialize the game board
def initialize_board():
    return [' ' for _ in range(9)]

def print_board(board):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")

def make_move(board, position, player):
    if board[position] == ' ':
        board[position] = player
        return True
    return False

def is_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_board_full(board):
    return ' ' not in board

# 1. Random AI (picks a random available move)
def random_ai_move(board):
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']
    if available_moves:
        move = random.choice(available_moves)
        make_move(board, move, 'O')

# 2. Minimax AI (chooses the best move based on Minimax algorithm)
def minimax(board, is_maximizing):
    if is_winner(board, 'O'):
        return 1
    if is_winner(board, 'X'):
        return -1
    if is_board_full(board):
        return 0

    available_moves = [i for i, spot in enumerate(board) if spot == ' ']

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves:
            board[move] = 'O'
            score = minimax(board, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves:
            board[move] = 'X'
            score = minimax(board, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def minimax_ai_move(board):
    best_score = -math.inf
    best_move = None
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']

    for move in available_moves:
        board[move] = 'O'
        score = minimax(board, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move

    if best_move is not None:
        make_move(board, best_move, 'O')

# 3. Monte Carlo Tree Search (MCTS) AI
def simulate_random_game(board, player):
    simulation_board = board[:]
    current_player = player

    while True:
        available_moves = [i for i, spot in enumerate(simulation_board) if spot == ' ']
        if not available_moves:
            break
        move = random.choice(available_moves)
        simulation_board[move] = current_player
        if is_winner(simulation_board, current_player):
            return current_player
        current_player = 'O' if current_player == 'X' else 'X'

    return None

def mcts_ai_move(board):
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']
    move_scores = {move: 0 for move in available_moves}

    for move in available_moves:
        wins = 0
        trials = 100  # Number of simulations
        for _ in range(trials):
            board_copy = board[:]
            make_move(board_copy, move, 'O')
            result = simulate_random_game(board_copy, 'X')
            if result == 'O':
                wins += 1
        move_scores[move] = wins / trials

    best_move = max(move_scores, key=move_scores.get)
    make_move(board, best_move, 'O')

# Main game loop
def tic_tac_toe():
    while True:
        board = initialize_board()
        print("Welcome to Tic-Tac-Toe!")
        print_board(board)

        # Choose AI algorithm
        print("\nChoose AI algorithm:")
        print("1. Random AI")
        print("2. Minimax AI")
        print("3. Monte Carlo Tree Search AI")
        ai_choice = input("Enter the number of the AI to play against (1-3): ")

        while True:
            # Human move
            move = int(input("Enter your move (1-9): ")) - 1
            if not make_move(board, move, 'X'):
                print("Invalid move! Try again.")
                continue

            print_board(board)

            if is_winner(board, 'X'):
                print("Congratulations! You win!")
                break
            if is_board_full(board):
                print("It's a tie!")
                break

            # AI move
            print("AI is making its move...")
            if ai_choice == '1':
                random_ai_move(board)
            elif ai_choice == '2':
                minimax_ai_move(board)
            elif ai_choice == '3':
                mcts_ai_move(board)

            print_board(board)

            if is_winner(board, 'O'):
                print("AI wins! Better luck next time.")
                break
            if is_board_full(board):
                print("It's a tie!")
                break

        # Ask if the player wants to play again
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

tic_tac_toe()
