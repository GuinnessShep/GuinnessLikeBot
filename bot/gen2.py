import random
import uuid
import sys
from time import time

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

        # Generate action_time (current timestamp rounded to nearest second)
        action_time = round(time())
        
        # Generate device_id with 19 digits
        device_id = ''.join(random.choice('0123456789') for _ in range(19))
        
        # Generate a random UUID
        id = uuid.uuid4()

        # Generate a random 16 digit hexadecimal
        hex = "%016x" % random.randint(0, 2**64-1)
        
        # Write the generated values to the file
        f.write(f"{action_time}:{device_id}:{id}:{hex}\n")

print("File 'devices.txt' has been successfully generated.")
