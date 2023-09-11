import tkinter as tk
from tkinter import messagebox
import random




# Define the game board and initialize it
board = [' ' for _ in range(9)]

# Define the winning combinations
winning_combinations = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)  # Diagonals
]

# Function to check if a player has won
def winCheck(player):
    for combo in winning_combinations:
        # Check if the player has marked all the positions in a winning combination
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

# Function to check if the game is a tie
def tieCheck():
    # Check if there are no empty spaces left on the board
    return ' ' not in board

# Function to make a move
def doMove(position, player):
    # Check if the position is empty before making a move
    if board[position] == ' ':
        board[position] = player

# Function to undo a move
def backMove(position):
    # Reset the position to an empty space
    board[position] = ' '


# Minimax Algorithm with Alpha-Beta Pruning
def minimax(position, depth, alpha, beta, maximizing_player):
    # Base cases: check if the game is over
    if depth == 0 or winCheck('X') or winCheck('O') or tieCheck():
        # If X wins, return 1
        if winCheck('X'):
            return 1
        # If O wins, return -1
        elif winCheck('O'):
            return -1
        # If it's a tie, return 0
        else:
            return 0
    
    if maximizing_player:
        max_eval = float('-inf')
        # Loop through all possible moves
        for move in range(9):
            if board[move] == ' ':
                doMove(move, 'X')  # Make the move for the maximizing player (X)
                # Recursively call minimax for the opponent (minimizing player) with updated depth and alpha-beta values
                eval = minimax(move, depth - 1, alpha, beta, False)
                backMove(move)  # Undo the move
                max_eval = max(max_eval, eval)  # Update the maximum evaluation
                alpha = max(alpha, eval)  # Update alpha
                if beta <= alpha:
                    break  # Alpha-beta pruning: stop evaluating remaining moves if beta <= alpha
        return max_eval
    else:
        min_eval = float('inf')
        # Loop through all possible moves
        for move in range(9):
            if board[move] == ' ':
                doMove(move, 'O')  # Make the move for the minimizing player (O)
                # Recursively call minimax for the opponent (maximizing player) with updated depth and alpha-beta values
                eval = minimax(move, depth - 1, alpha, beta, True)
                backMove(move)  # Undo the move
                min_eval = min(min_eval, eval)  # Update the minimum evaluation
                beta = min(beta, eval)  # Update beta
                if beta <= alpha:
                    break  # Alpha-beta pruning: stop evaluating remaining moves if beta <= alpha
        return min_eval


# Customizing the search algorithms to exploit domain-specific knowledge or heuristics
def evaluate_move(move):
    # Assign weights or scores to different moves based on their desirability
    weights = [
        3, 1, 3,
        1, 5, 1,
        3, 1, 3
    ]
    return weights[move]


# Function to find the best move using Minimax with Alpha-Beta Pruning
def find_best_move(difficulty):
    if difficulty == 'Easy':
        # Choose a random move from the available empty positions
        return random.choice([i for i, x in enumerate(board) if x == ' '])
    elif difficulty == 'Medium':
        best_eval = float('-inf')
        best_moves = []
        # Use the evaluate_move function to assign scores to available moves
        scores = [evaluate_move(move) if board[move] == ' ' else float('-inf') for move in range(9)]
        best_score = max(scores)
        best_moves = [move for move, score in enumerate(scores) if score == best_score]
        alpha = float('-inf')
        beta = float('inf')
        # Loop through all possible moves
        for move in range(9):
            if board[move] == ' ':
                doMove(move, 'X')  # Make the move for the maximizing player (X)
                # Recursively call minimax for the opponent (minimizing player) with updated depth and alpha-beta values
                eval = minimax(move, 5, alpha, beta, False)
                backMove(move)  # Undo the move
                if eval > best_eval:
                    best_eval = eval
                    best_moves = [move]  # Update the best move
                elif eval == best_eval:
                    best_moves.append(move)  # Add the move to the list of best moves
        return random.choice(best_moves)  # Choose a random move from the best moves
    elif difficulty == 'Hard':
        best_eval = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        # Loop through all possible moves
        for move in range(9):
            if board[move] == ' ':
                doMove(move, 'X')  # Make the move for the maximizing player (X)
                # Recursively call minimax for the opponent (minimizing player) with updated depth and alpha-beta values
                eval = minimax(move, 5, alpha, beta, False)
                backMove(move)  # Undo the move
                if eval > best_eval:
                    best_eval = eval
                    best_move = move  # Update the best move
                    alpha = max(alpha, eval)  # Update alpha
                    if beta <= alpha:
                        break  # Alpha-beta pruning: stop evaluating remaining moves if beta <= alpha
        return best_move  # Return the best move




# Create the main window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Define game metrics variables
total_games = 0
player_wins = 0
computer_wins = 0
ties = 0

# Function to update game metrics labels
def update_metrics(outcome):
    # Declare global variables to modify
    global total_games, player_wins, computer_wins, ties
    
    # Increment the total games count
    total_games += 1
    
    # Update the win/loss/tie counts based on the outcome
    if outcome == 'win':
        player_wins += 1
    elif outcome == 'lose':
        computer_wins += 1
    elif outcome == 'tie':
        ties += 1
    
    # Update the labels displaying the metrics
    total_games_label.config(text=str(total_games))
    player_wins_label.config(text=str(player_wins))
    computer_wins_label.config(text=str(computer_wins))
    ties_label.config(text=str(ties))
    
    # Calculate the win rates and update the labels
    player_win_rate = (player_wins / total_games) * 100 if total_games > 0 else 0
    computer_win_rate = (computer_wins / total_games) * 100 if total_games > 0 else 0
    tie_rate = (ties / total_games) * 100 if total_games > 0 else 0
    
    player_win_rate_label.config(text="Win Rate: {:.2f}%".format(player_win_rate))
    computer_win_rate_label.config(text="Win Rate: {:.2f}%".format(computer_win_rate))
    tie_rate_label.config(text="Tie Rate: {:.2f}%".format(tie_rate))


# Function to handle button click event
def handle_click(position):
    # Check if the clicked position is empty
    if board[position] == ' ':
        # Make a move for the player ('O')
        doMove(position, 'O')
        buttons[position].config(text='O', state=tk.DISABLED)
        
        # Check if the game is not over
        if not winCheck('O') and not tieCheck():
            # Get the selected difficulty level
            difficulty = difficulty_var.get()
            
            # Find the best move for the computer ('X')
            best_move = find_best_move(difficulty)
            
            # Make the best move for the computer
            doMove(best_move, 'X')
            buttons[best_move].config(text='X', state=tk.DISABLED)


                # Check if the player ('O') has won
        if winCheck('O'):
            messagebox.showinfo("Game Over", "You won!")
            update_metrics('win')
            reset_game()
        # Check if the computer ('X') has won
        elif winCheck('X'):
            messagebox.showinfo("Game Over", "You lost!")
            update_metrics('lose')
            reset_game()
        # Check if the game is a tie
        elif tieCheck():
            messagebox.showinfo("Game Over", "It's a tie!")
            update_metrics('tie')
            reset_game()

# Function to reset the game and update metrics labels
def reset_game():
    global board
    # Reset the game board
    board = [' ' for _ in range(9)]
    
    # Reset the buttons on the GUI
    for button in buttons:
        button.config(text=' ', state=tk.NORMAL)

    # Update metrics labels
    total_games_label.config(text="Total Games: {}".format(total_games))
    player_wins_label.config(text="Player Wins: {}".format(player_wins))
    computer_wins_label.config(text="Computer Wins: {}".format(computer_wins))
    ties_label.config(text="Ties: {}".format(ties))

    # Calculate win rates and update labels
    player_win_rate = (player_wins / total_games) * 100 if total_games > 0 else 0
    computer_win_rate = (computer_wins / total_games) * 100 if total_games > 0 else 0
    tie_rate = (ties / total_games) * 100 if total_games > 0 else 0

    player_win_rate_label.config(text="Player Win Rate: {:.2f}%".format(player_win_rate))
    computer_win_rate_label.config(text="Computer Win Rate: {:.2f}%".format(computer_win_rate))
    tie_rate_label.config(text="Tie Rate: {:.2f}%".format(tie_rate))


# Create the game board buttons
buttons = []
for i in range(9):
    button = tk.Button(window, text=" ", width=10, height=5, font=('Arial', 20, 'bold'), bg='#dcdcdd')

    buttons.append(button)

# Add button click event handlers
for i in range(9):
    buttons[i].config(command=lambda position=i: handle_click(position))

# Configure button layout
for i in range(3):
    for j in range(3):
        buttons[i * 3 + j].grid(row=i, column=j, padx=5, pady=5)

# Function to update the button colors



# Create the difficulty level selection
difficulty_var = tk.StringVar()
difficulty_label = tk.Label(window, text="Difficulty Level:", font=('Arial', 16, 'bold'),bg="#fff")
difficulty_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W) 

difficulty_options = ['Easy', 'Medium', 'Hard']
difficulty_dropdown = tk.OptionMenu(window, difficulty_var, *difficulty_options)
difficulty_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
difficulty_var.set('Medium')

# Create game metrics labels
metrics_frame = tk.Frame(window)
metrics_frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

total_games_label = tk.Label(metrics_frame, text="Total Games: 0", font=('Arial', 12))
total_games_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

player_wins_label = tk.Label(metrics_frame, text="Player Wins: 0", font=('Arial', 12))
player_wins_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

computer_wins_label = tk.Label(metrics_frame, text="Computer Wins: 0", font=('Arial', 12))
computer_wins_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

ties_label = tk.Label(metrics_frame, text="Ties: 0", font=('Arial', 12))
ties_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

player_win_rate_label = tk.Label(metrics_frame, text="Win Rate: 0.00%", font=('Arial', 12))
player_win_rate_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

computer_win_rate_label = tk.Label(metrics_frame, text="Win Rate: 0.00%", font=('Arial', 12))
computer_win_rate_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

tie_rate_label = tk.Label(metrics_frame, text="Tie Rate: 0.00%", font=('Arial', 12))
tie_rate_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Add some styling to the metrics labels
metrics_frame.configure(bg="#fff")  # Set background color
labels = [total_games_label, player_wins_label, computer_wins_label, ties_label, player_win_rate_label,
          computer_win_rate_label, tie_rate_label]
for label in labels:
    label.configure(fg="black", bg="#fff")  # Set text color and background color

# Customize the font and alignment of the labels
font = ('Arial', 12)
alignment = tk.W
for i in range(4):
    metrics_frame.grid_columnconfigure(i, weight=1)
    metrics_frame.grid_rowconfigure(i, weight=1)
    labels[i].config(font=font, anchor=alignment)
for i in range(4, 7):
    metrics_frame.grid_columnconfigure(i, weight=1)
    metrics_frame.grid_rowconfigure(i, weight=1)
    labels[i].config(font=font, anchor=alignment)

#Fixing the responsive layout

for i in range(4):
    window.grid_rowconfigure(i, weight=1, minsize=100)

for i in range(3):
    window.grid_columnconfigure(i, weight=1, minsize=100)


################################################################

# Start the main event loop
# Set the background color of the main window
window.configure(bg='#fff')

# Start the main event loop
window.mainloop()