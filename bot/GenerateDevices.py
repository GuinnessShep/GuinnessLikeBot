import random
import uuid
import sys

# Check if a command line argument is given
if len(sys.argv) > 1:
    try:
        num_lines = int(sys.argv[1])
    except ValueError:
        print("The given argument is not a valid number. Using default input method.")
        num_lines = int(input("How many lines do you want to generate? "))
else:
    num_lines = int(input("How many lines do you want to generate? "))

with open("devices.txt", "w") as f:
    for _ in range(num_lines):
        # Generate two random 19 digit numbers starting with 714
        num1 = 7140000000000000000 + random.randint(0, 999999999999999999)
        num2 = 7140000000000000000 + random.randint(0, 999999999999999999)
        
        # Generate a random UUID
        id = uuid.uuid4()

        # Generate a random 16 digit hexadecimal
        hex = "%016x" % random.randint(0, 2**64-1)
        
        # Write the generated values to the file
        f.write(f"{num1}:{num2}:{id}:{hex}\n")

print("File 'devices.txt' has been successfully generated.")
