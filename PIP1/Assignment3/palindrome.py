"""
Lab 3, Exercise 1: Write a function named is_palindrome that takes a single word (a string) as an argument and
checks if it is a palindrome. The function should return True if the word is a palindrome, and
False otherwise. The function should ignore the difference between uppercase and lowercase letters.
For instance, "Madam" should be considered a palindrome. The function should only consider letters, so punctuation
or spaces are not relevant in this case. (For simplicity, you can assume that input will only be a single word
without spaces or punctuation.)
"""
word = input("Enter a word to check if it is a palindrome: ")

def is_palindrome(word):
    word = word.lower()
    print(word == word[::-1])

is_palindrome(word)
