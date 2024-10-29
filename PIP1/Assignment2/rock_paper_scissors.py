import random

"""
Conditionals 7: Write a program that allows you to play a game of Rock, Paper, Scissors against a
computer. Use random library to select computer move.
"""

import random

intro_message = "Let's play the Rock, Paper, Scissors game!"
enter_choice = "Enter your choice (rock, paper, or scissors): "
tie_message = "It's a tie!"
win_message = "You win!"
lose_message = "You lose!"
scissors = "scissors"
paper = "paper"
rock = "rock"

def get_computer_choice():
    return random.choice([rock, paper, scissors])

def get_user_choice():
    choice = input(enter_choice).lower()
    while choice not in [rock, paper, scissors]:
        choice = input("Invalid choice! " + enter_choice).lower()

    return choice

def get_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        message = tie_message
    elif (user_choice == rock and computer_choice == scissors) or \
            (user_choice == paper and computer_choice == rock) or \
            (user_choice == scissors and computer_choice == paper):
        message = win_message
    else:
        message = lose_message

    return message

print(intro_message)
user_choice = get_user_choice()
computer_choice = get_computer_choice()

print("You chose: " + user_choice)
print("The computer chose: " + computer_choice)
result = get_winner(user_choice, computer_choice)
print(result)
