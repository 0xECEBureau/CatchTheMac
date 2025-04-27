import base64

def encode_100_times(input_string):
    encoded = input_string.encode()  # convert to bytes
    for _ in range(50):
        encoded = base64.b64encode(encoded)
    return encoded.decode()  # back to string

if __name__ == "__main__":
    flag = "MAC{buUUUuUuuuuUUUUcheEeeeeeEEEeeeeE}"
    result = encode_100_times(flag)
    with open("challenge.txt", "w") as f:
        f.write(result)
    print("[+] Encoded flag written to challenge.txt")
