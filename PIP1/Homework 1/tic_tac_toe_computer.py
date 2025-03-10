import random

"""
Homework 1 3: Modify exercise 2, second player is now computer that randomly selects valid move.
"""

import random


def draw_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def get_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None


def is_draw(board):
    return all(cell != " " for row in board for cell in row)


def get_computer_move(board):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(available_moves) if available_moves else None


def run_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_active = True

    while game_active:
        draw_board(board)

        if current_player == "X":
            try:
                row = int(input("Player X, enter the row (0-2): "))
                col = int(input("Player X, enter the column (0-2): "))

                if board[row][col] != " ":
                    print("Cell already taken! Try again.")
                    continue

                board[row][col] = current_player

            except (ValueError, IndexError):
                print("Invalid input. Please enter numbers between 0 and 2.")
                continue

        else:
            print("Computer's turn:")
            row, col = get_computer_move(board)
            board[row][col] = current_player
            print(f"Computer placed {current_player} at ({row}, {col})")

        winner = get_winner(board)

        if winner:
            draw_board(board)
            print(f"Player {winner} wins!")
            game_active = False
            break

        if is_draw(board):
            draw_board(board)
            print("It's a draw!")
            game_active = False
            break

        # Switch players
        current_player = "O" if current_player == "X" else "X"


run_game()

