"""
Conditionals 1: Given the prices of adult and child tickets, and three boolean values that indicate
whether the customers are adult, calculate and display the total amount to pay for the 3 tickets
"""

adult_price = 20
child_price = 10
total_amount = 0
is_adult_list = []

print("Bear in mind that answers other than 'yes/no' are considered as 'no'")
for i in range(1, 4):
    is_adult = input(f"Is customer {i} an adult? (yes/no): ").strip().lower() == "yes"
    is_adult_list.append(is_adult)

for is_adult in is_adult_list:
    if is_adult:
        total_amount += adult_price
    else:
        total_amount += child_price

print(f"Total amount to pay: ${total_amount:.2f}")
