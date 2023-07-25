import random
import uuid

def generate_line():
    part1 = random.randint(7140000000000000000, 7140000000000000000)
    part2 = random.randint(part1, part1 + random.randint(10000000000000000, 100000000000000000))
    part3 = str(uuid.uuid4())
    part4 = "%016x" % random.randint(0, 2**64 - 1)
    return f"{part1}:{part2}:{part3}:{part4}"

def main():
    num_lines = int(input("Enter the number of lines to generate: "))
    with open("devices.txt", "w") as f:
        for _ in range(num_lines):
            f.write(generate_line() + "\n")

if __name__ == "__main__":
    main()
