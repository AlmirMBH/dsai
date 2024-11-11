"""
Lab 3, Exercise 2: In this task, you will write a function that finds the second largest number in a list of numbers.
For example, if the list is [4, 6, 2, 8, 6], the largest number is 8, and the second largest is 6.
It is not allowed to use any other libraries (you can only initialize max and second_max
to float('-inf '), other than that you can not use any libraries or modules!
Write a function named find_second_largest that takes a list of numbers as an argument and
returns the second largest number in the list.
If the list has less than two unique elements, the function should return None.
The function should handle lists with duplicate values. For example, in the list [4, 6,
2, 8, 6], the second largest element is 6 even though it appears twice.
"""
def find_second_largest(numbers):
    unique_numbers = []
    for num in numbers:
        if num not in unique_numbers:
            unique_numbers.append(num)

    if len(unique_numbers) < 2:
        return None

    max_num = second_max = float('-inf')

    for num in unique_numbers:
        if num > max_num:
            second_max = max_num
            max_num = num
        elif num > second_max:
            second_max = num

    return second_max


print(find_second_largest([4, 6, 2, 8, 6]))  # Output: 6
print(find_second_largest([10, 20, 20, 5]))  # Output: 10
print(find_second_largest([3]))              # Output: None
print(find_second_largest([5, 5, 5]))        # Output: None

