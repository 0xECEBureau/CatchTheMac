flag = "MAC{un_s3ul_e7re_v0us_m4nqu3_3t_t0ut_3s7_depeupl3}"
binary = ''.join(format(ord(c), '08b') for c in flag)

output = ''
for bit in binary:
    if bit == '0':
        output += ' '
    else:
        output += '\t'

# Add a newline every 8 bits
output = '\n'.join([output[i:i+8] for i in range(0, len(output), 8)])

with open('message.txt', 'w') as f:
    f.write(output)
