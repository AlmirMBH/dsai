import re

"""
Conditionals 6: Write a program that asks the user to enter a password and validates it by the
following rules:
• Password must have at least 1 letter between [a-z] and 1 letter between [A-Z].
• Password must have at least 2 numbers between [0-9].
• Password length must be between 8 and 30 characters.
"""

def validate_password(password):
    message = ""
    password_valid = True

    # Length
    if len(password) < 8 or len(password) > 30:
        message += "The password must have between 8 and 30 characters!\n "
        password_valid = False

    # Lowercase
    elif not re.search(r'[a-z]', password):
        message += "The password must have at least one lowercase character!\n "
        password_valid = False

    # Uppercase
    elif not re.search(r'[A-Z]', password):
        message += "The password must have at least one uppercase character!\n "
        password_valid = False

    # Two digits
    elif len(re.findall(r'[0-9]', password)) < 2:
        message += "The password must have at least two numbers!\n "
        password_valid = False

     # Password OK
    else:
        message = "Password accepted!"
        password_valid = True

    return {"password_valid": password_valid, "message": message}


prompt = "Enter a password: "
password_input = input(prompt)
password = validate_password(password_input)

while not password["password_valid"]:
    password_input = input(password["message"] + prompt)
    password = validate_password(password_input)

if password["password_valid"]:
    print(password["message"])
else:
    print(password["message"])
