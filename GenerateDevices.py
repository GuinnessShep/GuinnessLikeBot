import random
import uuid

# Ask for the number of lines to generate
num_lines = int(input("How many lines would you like to generate? "))

# Open the file to write
with open('devices.txt', 'w') as f:
    # Generate the specified number of lines
    for _ in range(num_lines):
        # Generate the fields
        field1 = '714' + str(random.randint(1000000000000000000, 9999999999999999999))
        field2 = '714' + str(random.randint(1000000000000000000, 9999999999999999999))
        field3 = str(uuid.uuid4())
        field4 = ''.join([random.choice('0123456789abcdef') for _ in range(16)])

        # Write the line to the file
        f.write(f'{field1}:{field2}:{field3}:{field4}\n')

print(f"Generated {num_lines} lines in devices.txt.")
