import reedsolo

def encode_reed_solomon(data, nsym=8,max_nsym=32):
    """
    Encodes a list of bytes using Reed-Solomon codes.

    Args:
        data: A list of integers (bytes) between 0 and 255.
        nsym: The number of error correction symbols.

    Returns:
        A list of bytes representing the encoded data.
    """
    if nsym > max_nsym:
        nsym = max_nsym
        print(f"Error correction symbols limited to {max_nsym}")
    rs = reedsolo.RSCodec(nsym)
    encoded = rs.encode(bytes(data))
    return list(encoded)

def decode_reed_solomon(encoded_data, nsym=8,max_nsym=32):
    """
    Decodes a list of bytes using Reed-Solomon codes and corrects errors.

    Args:
        encoded_data: A list of integers (bytes) representing the encoded data.
        nsym: The number of error correction symbols.

    Returns:
        A tuple:
            - A list of bytes representing the decoded data.
            - The number of corrected errors.
            - True if the decoding was successful, false if there were too many errors.
    """
    if nsym > max_nsym:
        nsym = max_nsym
        print(f"Error correction symbols limited to {max_nsym}")
    rs = reedsolo.RSCodec(nsym)
    try:
        decoded = rs.decode(bytes(encoded_data))
        return list(decoded[0]), decoded[1], True
    except reedsolo.ReedSolomonError:
        return None, nsym + 1, False # Return None, nsym+1 for error count, and False to indicate failure.

# byteList = [4, 0, 0, 0, 46, 116, 120, 116, 104, 101, 121, 32, 116, 104, 101, 114, 101, 250, 110, 252]
# byteList = encode_reed_solomon(byteList,int(0.2*len(byteList)))
# byteList = [1, 0, 0, 0, 46, 116, 120, 116, 104, 101, 121, 32, 116, 104, 101, 114, 101, 250, 110, 252]
# b, errors_corrected, success = decode_reed_solomon(byteList,int(len(byteList)/6))
# print(b, errors_corrected, success,)
#a = encode_reed_solomon(,)
# a = a[:5] + [0] + a[5:]  # introduce an error
# b, errors_corrected, success = decode_reed_solomon(a)
# print(f"Decoded data: {b}",a)