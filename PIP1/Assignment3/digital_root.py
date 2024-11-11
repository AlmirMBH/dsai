"""
Group 1: Exercise 3: Implement a function that calculates the digital root of a non-negative integer, which is the
sum of its digits repeated until only one digit remains.
Example: digital_root(9875) = 2 (since 9+8+7+5=29 and 2+9=11 and 1+1=2).
"""
def digital_root(n):
    if n < 10:
        return n
    else:
        return digital_root(sum(int(digit) for digit in str(n))) # convert to string to loop through

print(digital_root(9875))  # Output: 2
