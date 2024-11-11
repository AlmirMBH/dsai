"""
Group 4, Exercise 4: Implement a function gcd_three(a, b, c) that returns the greatest common divisor of three
integers. Use the property that gcd(a, b, c) = gcd(gcd(a, b), c). Use function that you have
already implemented in second assignment.
"""
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def gcd_three(a, b, c):
    return gcd(gcd(a, b), c)

print(gcd_three(24, 36, 60))
