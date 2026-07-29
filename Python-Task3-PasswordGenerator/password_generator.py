# built-in python module used to generate random things
import random   

# python built-in module containing all alphabets,numbers and special characters
import string 

print("----Password Generator-----")

try:
    length = int(input("Enter password length: "))

    if length < 8:
        print("Password length must be at least 8 characters.")

    else:
        characters = string.ascii_letters + string.digits + string.punctuation

        password = ""

        for i in range(length):
            password += random.choice(characters)

        print("\nGenerated Password:", password)
        print("Password length:", length)

except ValueError:
    print("Invalid input! Please enter a whole number.")