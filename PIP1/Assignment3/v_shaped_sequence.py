"""
Group 1, Exercise 1: Implement a Python function that takes a list of numbers as input and returns a boolean value,
True or False. The function should return True if the list is a strict "V-shaped" sequence,
meaning the elements in the list first strictly decrease to a certain point and then strictly increase
from that point onward. If the list does not satisfy this condition, the function should return
False. It is assumed that the list contains only numbers, so input validation is not necessary.
Note: a sorted list that only increases or only decreases is not considered a V-shaped sequence.
"""
def is_v_shaped_sequence(numbers):
    n = len(numbers)

    if n < 3:
        return False

    min_index = numbers.index(min(numbers))

    # The lowest number in the initial or final position eliminates v-shape
    if min_index == 0 or min_index == n - 1:
        return False

    for i in range(1, min_index + 1):
        if numbers[i] >= numbers[i - 1]:  # numbers must be decreasing (no duplicates)
            return False

    for i in range(min_index + 1, n):
        if numbers[i] <= numbers[i - 1]:  # numbers must be increasing (no duplicates)
            return False

    return True

print(is_v_shaped_sequence([5, 3, 1, 2, 4]))  # Output: True
print(is_v_shaped_sequence([10, 8, 5, 3, 6, 9]))  # Output: True
print(is_v_shaped_sequence([1, 2, 3, 4, 5]))  # Output: False
print(is_v_shaped_sequence([5, 4, 3, 2, 1]))  # Output: False
print(is_v_shaped_sequence([2, 1, 1, 2, 3]))  # Output: False
print(is_v_shaped_sequence([2, 1, 7, 8, 8]))  # Output: False
