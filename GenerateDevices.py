import uuid

def generate_device_identifiers(num_identifiers):
    identifiers = []
    for _ in range(num_identifiers):
        did = str(uuid.uuid4().int)
        iid = str(uuid.uuid4().int)
        cdid = str(uuid.uuid4())
        openudid = str(uuid.uuid4())
        identifier = f"{did}:{iid}:{cdid}:{openudid}"
        identifiers.append(identifier)
    return identifiers

def save_identifiers_to_file(identifiers):
    with open("devices.txt", "w") as file:
        for identifier in identifiers:
            file.write(identifier + "\n")

# Prompt the user for the number of identifiers to generate
num_identifiers = int(input("How many identifiers do you want to generate? "))

# Generate the identifiers
identifiers = generate_device_identifiers(num_identifiers)

# Save the identifiers to a file
save_identifiers_to_file(identifiers)

print(f"{num_identifiers} unique identifiers have been generated and saved to devices.txt.")
