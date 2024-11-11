"""
Group 4, Exercise 2: Implement a recursive function gcd(a, b) that finds greatest common divisor of two numbers
(NZD). Do not use any built-in Python functions from any library (like math.gcd …)
Examples:
• gcd(48, 18)=6
• gcd(17, 51)=17
• gcd(21, 89)=1
"""
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)



print(gcd(48, 18))  # Output: 6
print(gcd(17, 51))  # Output: 17
print(gcd(21, 89))  # Output: 1
