def extract_device_info(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            entries = line.strip("{}\n").replace("'", "").split(', ')
            
            device_info = {'device_id': '', 'iid': '', 'cdid': '', 'openudid': ''}

            for entry in entries:
                key, value = entry.split(': ', 1)
                key = key.strip()

                if key in device_info:
                    device_info[key] = value.strip()

            file.write(f"{device_info['device_id']}:{device_info['iid']}:{device_info['cdid']}:{device_info['openudid']}\n")

extract_device_info('input.txt', 'devices1.txt')
