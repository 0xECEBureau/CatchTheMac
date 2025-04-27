def decode_whitespace_file(filename):
    with open(filename, 'r') as f:
        data = f.read()

    binary_string = ''
    for char in data:
        if char == ' ':
            binary_string += '0'
        elif char == '\t':
            binary_string += '1'
        elif char == '\n':
            # when we hit newline, process the 8-bit chunk
            if len(binary_string) == 8:
                ascii_char = chr(int(binary_string, 2))
                print(ascii_char, end='')
                binary_string = ''
        else:
            # ignore any other characters just in case
            continue

    print()

if __name__ == "__main__":
    decode_whitespace_file('message.txt')
