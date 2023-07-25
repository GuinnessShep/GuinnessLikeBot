import random
import uuid

def generate_line():
    # Generate two random large numbers
    num1 = random.randint(10**18, 10**19)
    num2 = random.randint(10**18, 10**19)

    # Generate a random UUID
    uid = uuid.uuid4()

    # Generate a random hex string
    hex_str = ''.join([random.choice('0123456789abcdef') for _ in range(16)])

    return f"{num1}:{num2}:{uid}:{hex_str}"

def main():
    num_lines = int(input("How many lines to generate? "))
    with open("devices.txt", "w") as f:
        for _ in range(num_lines):
            line = generate_line()
            f.write(line + "\n")
    print(f"Generated {num_lines} lines in 'devices.txt'")

if __name__ == "__main__":
    main()
