import serial,protect,converter
ser = serial.Serial(port = "COM5", baudrate=115200, bytesize=8, timeout=.2, stopbits=serial.STOPBITS_ONE)
readLine = ""
print("Waiting for data...")
while readLine=="":
    bs = ser.readline()
    readLine = bs.decode("utf-8").rstrip()
    if readLine!="":
        break
count = 0

print((readLine),end="")
values = [int(readLine.split(",")[1])]
while count<30:
    bs = ser.readline()
    readLine = bs.decode("utf-8").rstrip()
    if readLine=="":
        count += 1
    else:
        count = 0
        split = readLine.split(",")
        values.append(int(split[1]))
        print("       ",end="\r")
        print(readLine,end="\r")
print("Data recieved")
print("Number of values recieved: ",len(values))
values,errors,success = protect.decode_reed_solomon(values,round(len(values)*(0.2/1.2)))
if not success:
    print("Error decoding data, the file was messed up beyond repair")
    exit() 
converter.bytes_to_file_with_type(bytes(values))