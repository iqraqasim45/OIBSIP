import random
import string

print("----- Random Password Generator -----")

while True:

    try:
        # Ask for password length
        length = int(input("\nEnter password length (minimum 8): "))

        if length < 8:
            print("Password length must be at least 8 characters.")
            continue

        # Ask user to choose character types
        print("\nChoose character types:")
        print("1 - Uppercase letters (A-Z)")
        print("2 - Lowercase letters (a-z)")
        print("3 - Numbers (0-9)")
        print("4 - Symbols (!, @, #, $, etc.)")

        choices = input("Enter at least 2 choices, separated by commas: ")

        # Remove spaces and split choices
        choices = choices.replace(" ", "")
        choices = choices.split(",")

        # Check choices
        valid_choices = ["1", "2", "3", "4"]

        if any(choice not in valid_choices for choice in choices):
            print("Invalid choice! Please select only 1, 2, 3, or 4.")
            continue

        # Remove duplicate choices
        choices = list(set(choices))

        # At least 2 types are required
        if len(choices) < 2:
            print("Please select at least 2 character types.")
            continue

        # Create character groups
        groups = []

        if "1" in choices:
            groups.append(string.ascii_uppercase)

        if "2" in choices:
            groups.append(string.ascii_lowercase)

        if "3" in choices:
            groups.append(string.digits)

        if "4" in choices:
            groups.append(string.punctuation)

        # Make sure password is long enough
        if length < len(groups):
            print("Password length is too short for the selected character types.")
            continue

        # Add at least one character from every selected type
        password_characters = []

        for group in groups:
            password_characters.append(random.choice(group))

        # Fill the remaining password characters randomly
        all_characters = "".join(groups)

        for i in range(length - len(password_characters)):
            password_characters.append(random.choice(all_characters))

        # Shuffle the password so required characters are not always at the beginning
        random.shuffle(password_characters)

        password = "".join(password_characters)

        print("\nGenerated Password:", password)
        print("Password Length:", len(password))

        # Ask whether to generate another password
        again = input("\nGenerate another password? (yes/no): ")

        if again.lower() != "yes":
            print("Thank you for using the Password Generator!")
            break

    except ValueError:
        print("Invalid input! Please enter a valid number for password length.")