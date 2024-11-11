"""
Group 4, Exercise 1: Implement a Python function that takes a list of numbers as input and returns a boolean value,
True or False. The function should return True if the list is a strict "A-shaped" sequence,
meaning the elements in the list first strictly increase to a certain point and then strictly decrease
from that point onward. If the list does not satisfy this condition, the function should return
False. It is assumed that the list contains only numbers, so input validation is not necessary.
Note: a sorted list that only increases or only decreases is not considered an A-shaped sequence.
An "A-shaped" sequence is a sequence of numbers that has a single peak point where it
switches from strictly increasing to strictly decreasing. This means that, starting from the
beginning, each element is greater than the previous one until a maximum point is reached.
After this maximum, each element must be less than the previous one. Importantly, a sequence
that is entirely sorted (only increasing or only decreasing) does not qualify as A-shaped, since
it lacks the peak where it changes direction.
"""
def is_a_shaped_sequence(numbers):
    n = len(numbers)

    if n < 3:
        return False

    peak_index = numbers.index(max(numbers))

    # The peak in the first or last position eliminates A-shape
    if peak_index == 0 or peak_index == n - 1:
        return False

    for i in range(1, peak_index + 1):
        if numbers[i] <= numbers[i - 1]:  # Must be increasing (no duplicates)
            return False

    for i in range(peak_index + 1, n):
        if numbers[i] >= numbers[i - 1]:  # Must be decreasing (no duplicates)
            return False

    return True

print(is_a_shaped_sequence([1, 3, 5, 4, 2]))  # Output: True
print(is_a_shaped_sequence([2, 4, 6, 5, 3, 1]))  # Output: True
print(is_a_shaped_sequence([1, 2, 3, 4, 5]))  # Output: False
print(is_a_shaped_sequence([5, 4, 3, 2, 1]))  # Output: False
print(is_a_shaped_sequence([1, 3, 5, 5, 2, 1]))  # Output: False
print(is_a_shaped_sequence([1, 3, 7, 4, 2, 2, 1]))  # Output: False
