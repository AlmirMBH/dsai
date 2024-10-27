"""
Exercise 4: Write a program to convert temperatures to and from Celsius and Fahrenheit.
"""

# Functions
def validate_conversion_type(choice_input):
    while not choice_input.isalpha() or not choice_input in available_choices:
        choice_input = input("Invalid input! Please enter 'CF' or 'FC: ")

    return choice_input

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def validate_temperature(prompt):
    temperature_input = input(prompt)

    while not (temperature_input.replace('.', '', 1).isdigit() and temperature_input.count('.') <= 1):
        temperature_input = input("Invalid input! " + prompt)

    return float(temperature_input)


def convert_temperature(temperature, choice):
    if choice == 'CF':
        fahrenheit = celsius_to_fahrenheit(float(temperature))
        print(f"{temperature}°C is equal to {fahrenheit:.2f}°F")
    else:
        celsius = fahrenheit_to_celsius(float(temperature))
        print(f"{temperature}°F is equal to {celsius:.2f}°C")


# Prompts and function calls
print("CF: Convert Celsius to Fahrenheit\nFC: Convert Fahrenheit to Celsius")

temperature = 0
available_choices = ['CF', 'FC']
choice_input = input("Choose an option (CF or FC): ")
choice = validate_conversion_type(choice_input)

if choice == 'CF':
    temperature = validate_temperature("Enter temperature in Celsius: ")
elif choice == 'FC':
    temperature = validate_temperature("Enter temperature in Fahrenheit: ")

convert_temperature(temperature, choice)

