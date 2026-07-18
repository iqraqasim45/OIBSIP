try:

    weight = float(input("Enter your weight in Kg: "))
    height = float(input("Enter your height in meters: "))

    if weight <= 0 or height <= 0:
        print("Weight and Height must be greater than zero. It cannot be negative!")

    else:
        bmi = weight / (height ** 2)

        print("BMI is:", round(bmi, 2))

        if bmi < 18.5:
            print("You are in Underweight category!")

        elif bmi < 25:
            print("You are in Healthy category!")

        elif bmi < 30:
            print("You are in Overweight category!")

        else:
            print("You are Obese!")

except ValueError:
    print("Invalid input! Enter only positive numbers.")