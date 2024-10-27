# console input
age = int(input("Please enter age: "))

if age > 18:
    print("You are eligible to drive")
elif age < 18:
    print("You are not eligible to drive")

# list can be modified during the runtime
numbers = [1, 2, 3, 4, 5]

# for loop
for number in numbers:
    if number > 2:
        print("the element " + str(number) + " is greater than 2")

# while
count = 0
while count < 5:
    print("The number is: " + str(count))
    count+=1

# functions
def sum_of_list_elements(number_list):
    numbers_sum = 0
    for num in numbers:
        numbers_sum+=num

    print("The sum of list elements is: " + str(numbers_sum))

sum_of_list_elements([1, 2, 3, 4, 5])


def arithmetic_mean(n):
    sum = 0

    for i in range(1, n+1):
        sum+=i
    return sum/n

def main():
    n = int(input("Enter a number between 0 and 15: "))

    while n <= 0 or n > 15:
        if n <= 0:
            print(f"The number {n} must be greater than 0.")
        elif n > 15:
            print(f"The number {n} must be smaller than or equal to 15.")
        n = int(input("Please enter a valid number between 0 and 15: "))  # Keep asking for input

    print(f"The arithmetic mean is {arithmetic_mean(n)}")

main()

