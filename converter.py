import os
import struct

def file_to_bytes_with_type(filepath):
    """
    Reads a file, converts it to bytes, and includes the file extension.

    Args:
        filepath (str): The path to the file.

    Returns:
        bytes: The file extension length, extension bytes, and file content as bytes, or None if an error occurs.
    """
    try:
        _, file_extension = os.path.splitext(filepath)
        file_extension = file_extension.encode('utf-8')  # Encode extension to bytes
        extension_length = len(file_extension)

        with open(filepath, 'rb') as file:
            file_bytes = file.read()

        # Pack the extension length, extension, and file data into a single byte array.
        return struct.pack('I', extension_length) + file_extension + file_bytes

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def bytes_to_file_with_type(byte_data, output_directory="."):
    """
    Writes byte data to a file, extracting the file extension.

    Args:
        byte_data (bytes): The byte data to write.
        output_directory (str): The directory to save the file.
    """
    try:
        extension_length = struct.unpack('I', byte_data[:4])[0] #unpack the length
        extension_bytes = byte_data[4:4 + extension_length]
        file_extension = extension_bytes.decode('utf-8') #decode the extension
        file_bytes = byte_data[4 + extension_length:]

        output_filepath = os.path.join(output_directory, f"received_file{file_extension}")

        with open(output_filepath, 'wb') as file:
            file.write(file_bytes)

        print(f"File successfully written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")


# csv_bytes_with_type = file_to_bytes_with_type("testFile.py")
# print(bytes(list(csv_bytes_with_type)))
# if csv_bytes_with_type:
#     print(f"Simulating sending {len(csv_bytes_with_type)} bytes...")
#     received_csv_bytes_with_type = csv_bytes_with_type
#     print(f"Simulating receiving {len(received_csv_bytes_with_type)} bytes...")
#     bytes_to_file_with_type(received_csv_bytes_with_type, ".")