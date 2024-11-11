"""
Group 2, Exercise 3: Write a function count_divisible_by_digit_sum(start, end) that counts how many numbers in
the range [start, end] are divisible by the sum of their own digits.
"""

def digit_sum(n):
    return sum(int(digit) for digit in str(n))

def count_divisible_by_digit_sum(start, end):
    count = 0
    for number in range(start, end + 1):
        sum_of_digits = digit_sum(number)
        if sum_of_digits != 0 and number % sum_of_digits == 0:
            count += 1
    return count

# Example usage
print(count_divisible_by_digit_sum(1, 20))  # Output: count of numbers divisible by their digit sum
