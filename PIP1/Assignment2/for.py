"""
A for loop is used when we know the maximum number of repetitions in advance. It
can also be used to go through (iterate over) an entire sequence (a list, string, range, ...).
"""
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
num_of_attempts = 5
digit = -1
invalid_input = True

for num_of_attempts in range(num_of_attempts, 0, -1):
    if invalid_input:
        digit = input(f"You have {num_of_attempts} more attempts. Please enter a digit: ")
        if digit in digits:
            digit = int(digit)
            invalid_input = False
            break
        else:
            print("Invalid input")

    num_of_attempts -= 1
if invalid_input: print("No more attempts allowed.")
else: print(f"Thank you! You chose number {digit_names[digit]}")

print("String iteration")
text = "The same iterating logic applies to strings and other iterable objects"
vowels = "aeiou"
for char in text:
    print(char.upper(), end="") if char in vowels else print(char, end="")