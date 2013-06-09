def serial_to_wiegand(serial_tag):
    # drop protocol bits and convert to binary string (sans '0b')
    bin_string = bin(int(serial_tag[4:-5], base=16))[2:]
    even = bin_string[:12]  # split even and odd parity sections
    odd = bin_string[12:]   # per wiegand
    wiegand_tag = hex(   # convert to hex string to match db
        int(
            str(even.count('1') % 2) + even +  # add even parity bit
            odd + str(odd.count('1') % 2 ^ 1),  # add odd parity bit
            base=2
        )
    )[2:].upper()
    return wiegand_tag