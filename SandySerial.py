import serial
import serial.tools.list_ports
from datetime import datetime
import os
if not os.path.exists("ErrorLogs.csv"):
    with open("ErrorLogs.csv", "a") as f:
        f.write("Version,Date,Type,Log")
ports = list(serial.tools.list_ports.comports())
found = False
for p in ports:
    if 'USB-SERIAL CH340' in p.description:
        found = True
        ser = serial.Serial(p.device,9600,timeout=0.5)
if not found:
    print("We couldn't find the Arduino Nano. Put the port name you see under the title on the Hack Pack IDE into the port_name variable")
    port_name = "We couldn't find the Arduino Nano. Put the port name you see under the title on the Hack Pack IDE right here"
    ser = serial.Serial(port_name, 9600, timeout=0.5)
def waitTillnRecieved(n:str):
    readLine = "" if n != "" else " "
    while readLine!=n:
        bs = ser.readline()
        readLine = bs.decode("utf-8").rstrip()
def printSerial(a):
    now = datetime.now()
    with open("ErrorLogs.csv", "a") as f:
        f.write("\n1,"+str(datetime.timestamp(now))+",Serial Send"+","+a)
    ser.write(str(a).encode('utf-8'))

waitTillnRecieved("colo")
printSerial("<n>")
waitTillnRecieved("confirming!")
angle = 0
position = 0
printSerial("<"+str(angle)+">")
waitTillnRecieved(str(angle))
printSerial("<"+str(position)+">")
waitTillnRecieved(str(position))
waitTillnRecieved("done")
x=0
prevAngle = -1
prevPosition = -1
while x<2000:
    if prevAngle != angle or prevPosition != position:
        # print("Moving to {} mm at {} degrees".format(position,angle))
        printSerial("<"+str(angle)+">")
        waitTillnRecieved(str(angle))
        printSerial("<"+str(angle)+">")
        waitTillnRecieved(str(angle))
        printSerial("<"+str(position)+">")
        waitTillnRecieved(str(position))
        waitTillnRecieved("done")
    prevAngle = angle
    prevPosition = position
    error = 1
    while error != 0:
        try:
            file = open("liveDrawComms.txt","r")
            a = file.read()
            file.close()
            error = 0
        except BaseException as e:
            now = datetime.now()
            print(f"An error occurred while reading all positions: {e}")
            with open("ErrorLogs.csv", "a") as f:
                f.write("\n1,"+str(datetime.timestamp(now))+",Read Error"+","+str(e))
            error=1
    a = a.split("\n")
    b = a[0].split(",")
    try:
        position=int(b[1])
        angle=int(b[0])
    except IndexError as e:
        pass
        # now = datetime.now()
        # with open("ErrorLogs.csv", "a") as f:
        #     f.write("\n1,"+str(datetime.timestamp(now))+",Convert to Integer Error"+","+str(e))
    except ValueError as e:
        now = datetime.now()
        print("Values lost due to too fast reading of serial port. Need to build code to fix.")
        with open("ErrorLogs.csv", "a") as f:
            f.write("\n1,"+str(datetime.timestamp(now))+",Convert to Integer Error"+","+str(e))
    except BaseException as e:
        now = datetime.now()
        with open("ErrorLogs.csv", "a") as f:
            f.write("\n1,"+str(datetime.timestamp(now))+",Convert to Integer Error"+","+str(e))
    error = 1
    while error != 0:
        try:
            with open("liveDrawComms.txt", 'r') as f:
                lines = f.readlines()
            error = 0
        except BaseException as e:
            now = datetime.now()
            print(f"An error occurred while clearing reading all positions: {e}")
            with open("ErrorLogs.csv", "a") as f:
                f.write("\n1,"+str(datetime.timestamp(now))+",Clear Error"+","+str(e))
            error=1
    error = 1
    while error != 0:
        try:
            with open("liveDrawComms.txt", 'w') as f:
                f.writelines(lines[1:])
            error = 0
        except BaseException as e:
            print(f"An error occurred while clearing first positions: {e}")
            now = datetime.now()
            with open("ErrorLogs.csv", "a") as f:
                f.write("\n1,"+str(datetime.timestamp(now))+",First Clear Error"+","+str(e))
            error=1
    