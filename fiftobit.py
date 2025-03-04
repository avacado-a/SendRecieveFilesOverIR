#Not used in the final code
def bytes_to_bitstring(byte_list):
    """
  Converts a list of bytes (integers between 0-255) to a string of bits.

  Args:
    byte_list: A list of integers representing bytes.

  Returns:
    A string of '0's and '1's representing the bits.
    """
    bitstring = ""
    for byte in byte_list:
        if not isinstance(byte, int) or byte < 0 or byte > 255:
            raise ValueError("Input list must contain integers between 0 and 255.")
        bitstring += bin(byte)[2:].zfill(8)  # Convert to binary, remove '0b', pad with leading zeros

    return bitstring
def bitstring_to_bytes(bitstring):
    """
  Converts a string of bits ('0's and '1's) to a list of bytes.

  Args:
    bitstring: A string of '0's and '1's representing the bits.

  Returns:
    A list of integers representing the bytes.
    """
    if len(bitstring) % 8 != 0:
        raise ValueError("Bitstring length must be a multiple of 8.")

    bytes_list = []
    for i in range(0, len(bitstring), 8):
        byte_str = bitstring[i:i+8]
        byte = int(byte_str, 2)  # Convert binary string to integer
        bytes_list.append(byte)

    return bytes_list

def number_list_to_bitstring(number_list):
  """
  Converts a list of 15-bit numbers to a single bitstring.

  Args:
    number_list: A list of integers, each representing a 15-bit number.

  Returns:
    A string of '0's and '1's representing the concatenated bitstrings.
  """
  bitstring = ""
  for number in number_list:
    if number < 0 or number >= 2**15:
      raise ValueError("Numbers in the list must be between 0 and 32767 (inclusive).")
    bitstring += bin(number)[2:].zfill(15)  # Convert to binary, remove '0b', pad with zeros
  return bitstring
def bytes_to_number_list(byte_list):
    bit_string = bytes_to_bitstring(byte_list)
    bit_string+="1"
    while len(bit_string)%15!=0:
        bit_string+="0"
    number_list = [int(bit_string[i:i+15], 2) for i in range(0,len(bit_string),15)]
    return number_list
def number_list_to_bytes(number_list):
    bit_string = number_list_to_bitstring(number_list)
    while bit_string[len(bit_string)-1]=="0":
        bit_string=bit_string[:len(bit_string)-1]
    bit_string=bit_string[:len(bit_string)-1]
    byte_list = bitstring_to_bytes(bit_string)
    return byte_list
# Example usage:
# byte_list = [65, 66, 67, 10, 0, 255] # Example bytes
# print(byte_list)
# number_list = bytes_to_number_list(byte_list)
# print(number_list)
# byte_list = number_list_to_bytes(number_list)
# print(byte_list)