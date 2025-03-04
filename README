# Warning: this is an AI generated README.md file. It may not be accurate.
This project demonstrates a system for transferring files over Infrared (IR) communication using Arduino and Python. The project includes encoding and decoding files, error correction using Reed-Solomon codes, and serial communication between a computer and Arduino devices.

## Table of Contents

- Project Structure
- Setup
- Usage
- Files Description
- License

## Project Structure

```
.
├── __pycache__/
├── SendAndRecieveFilesOverIR/
│   ├── SignalReceiver/
│   │   └── SignalReceiver.ino
│   ├── SignalSender/
│   │   └── SignalSender_copy_20250303214306.ino
├── converter.py
├── fiftobit.py
├── getFile.py
├── protect.py
├── reference.py
├── SandySerial.py
├── sendFile.py
├── test.txt
└── /c:/Users/sidhp/AppData/Local/Programs/Python/Python312/Lib/site-packages/serial/serialwin32.py
```

## Setup

### Arduino

1. Open the Arduino IDE.
2. Load the SignalReceiver.ino file from SignalReceiver.
3. Load the SignalSender_copy_20250303214306.ino file from SignalSender.
4. Upload the respective sketches to your Arduino devices.

### Python

1. Ensure you have Python 3.12 installed.
2. Install the required Python packages:
   ```sh
   pip install pyserial reedsolo
   ```

## Usage

### Sending a File

1. Run the sendFile.py script:
   ```sh
   python sendFile.py
   ```
2. Enter the file name you want to send when prompted.

### Receiving a File

1. Run the getFile.py script:
   ```sh
   python getFile.py
   ```
2. The script will wait for data and decode the received file.

### Additional Scripts

- reference.py: Contains utility functions for adding, reading, and clearing positions in a communication file.
- SandySerial.py: Handles serial communication and logs errors.
- converter.py: Converts files to bytes and vice versa, including file extension handling.
- protect.py: Implements Reed-Solomon encoding and decoding for error correction.
- fiftobit.py: Contains functions for converting bytes to bitstrings and vice versa (not used in the final code).

## Files Description

- **SendAndRecieveFilesOverIR/SignalReceiver/SignalReceiver.ino**: Arduino code for receiving IR signals.
- **SendAndRecieveFilesOverIR/SignalSender/SignalSender_copy_20250303214306.ino**: Arduino code for sending IR signals.
- **converter.py**: Functions to convert files to bytes and back, including file extension handling.
- **fiftobit.py**: Functions for converting bytes to bitstrings and vice versa (not used in the final code).
- **getFile.py**: Script to receive a file over serial communication and decode it.
- **protect.py**: Functions for Reed-Solomon encoding and decoding for error correction.
- **reference.py**: Utility functions for managing positions in a communication file.
- **SandySerial.py**: Handles serial communication and logs errors.
- **sendFile.py**: Script to send a file over serial communication.
- **test.txt**: Sample text file used for testing.
- **/c:/Users/sidhp/AppData/Local/Programs/Python/Python312/Lib/site-packages/serial/serialwin32.py**: Serial communication backend for Windows.

## License

This project is licensed under the MIT License. See the SignalReceiver.ino and SignalSender_copy_20250303214306.ino files for more details.

avacado-a: @GitHubCopilot 

GitHub Copilot: There is no conversation provided to infer the user's goal. Please provide the conversation or specify the requirements so I can assist you accordingly.
