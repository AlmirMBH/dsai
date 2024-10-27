"""
Since the number of iterations is not explicitly limited, it is imperative to ensure that the
condition will eventually become false in order to end the loop. If that is not ensured, an
infinite loop can occur.
"""

digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
num_of_attempts = 5
digit = -1
invalid_input = True

while num_of_attempts > 0 and invalid_input:
    digit = input(f"You have {num_of_attempts} more attempts. Please enter a digit: ")
    if digit in digits:
        digit = int(digit)
        invalid_input = False
        break
    else:
        print("Invalid input")
    num_of_attempts -= 1
if invalid_input: print("No more attempts allowed.")
else: print(f"Thank you! You chose number {digit_names[digit]}")


wishes = ["love", "health", "happiness", "money", "home"]
granted = 0
offered = 0
print("You found a genie!")

while offered <5:
    choice = input(f"You have {3-granted} wishes left. Do you want {wishes[offered]}? [yes/no]: ")
    offered += 1
    if choice == "no": continue
    granted += 1
    if granted == 3: break

wishes = []
print("You can choose up to 10 wishes")
while True:
    elem = input("Enter your next wish. Type 'exit' to exit: ")
    if elem == "exit": break
    wishes.append(elem)
    if len(wishes) == 3: break

print("You chose (index): ")
for i in range(len(wishes)):
    print(f"{i+1:2}:", wishes[i])

print("You chose (enumerate): ")
for i, wish in enumerate(wishes):
    print(f"{i+1:2}-->", wish)

print("You chose (bullet point): ")
for wish in wishes:
    print("-", wish)
