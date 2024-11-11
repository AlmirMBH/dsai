"""
Group 1, Exercise 4: Implement a function lcm(a, b) that calculates the least common multiple of two integers.
You can use the relationship lcm(a, b)=∣a⋅ b∣ / gcd(a, b).
Example: lcm(12, 18) = 36.
"""
def lcm(a, b):
    def gcd(x, y):
        if y == 0:
            return x
        return gcd(y, x % y)

    return abs(a * b) // gcd(a, b)


print(lcm(12, 18))  # Output: 36

