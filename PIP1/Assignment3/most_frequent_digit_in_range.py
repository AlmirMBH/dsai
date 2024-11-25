"""
Group 4, Exercise 3: Write a function most_frequent_digit_in_range(start, end) that returns the most frequent digit
across all numbers in the range [start, end].
"""
def most_frequent_digit_in_range(start, end):
    digit_count = {}

    for number in range(start, end + 1):
        for digit in str(number):
            digit_count[int(digit)] = digit_count.get(digit, 0) + 1

    most_frequent_digit = max(digit_count, key=digit_count.get)
    return most_frequent_digit

print(most_frequent_digit_in_range(20, 30))
