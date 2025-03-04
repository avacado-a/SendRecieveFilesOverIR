import converter
import serial
import protect
file_name = input("Enter the file name: ")
byteList = list(converter.file_to_bytes_with_type(file_name))
byteList = protect.encode_reed_solomon(byteList,round(0.2*len(byteList)))
print("Number of bytes being transfered: ",len(byteList))
ser = serial.Serial(port = "COM8", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
def waitTillnRecieved(n:str):
    readLine = "" if n != "" else " "
    while readLine!=n:
        bs = ser.readline()
        readLine = bs.decode("utf-8").rstrip()
def printSerial(a):
    ser.write(str(a).encode('utf-8'))
def loading_bar(progress, total, bar_length=50):
    percent = 100 * (progress / float(total))
    arrow = '█' * int(percent/100 * bar_length )
    spaces = ' ' * (bar_length - len(arrow))
    print(f'Progress: |{arrow}{spaces}| {percent:.2f}%', end='\r')
waitTillnRecieved("colo")
printSerial("<n>")
waitTillnRecieved("confirming!")
test = 8
byte = byteList[0]
count = 0
#printSerial("<"+str(test)+">")
#waitTillnRecieved(str(test))
printSerial("<"+str(byte)+">")
waitTillnRecieved(str(byte))
waitTillnRecieved("done")
for x in range(1,len(byteList)):
    loading_bar(x,len(byteList[:]))
    byte=int(byteList[x])
    #printSerial("<"+str(test)+">")
    #waitTillnRecieved(str(test))
    printSerial("<"+str(byte)+">")
    waitTillnRecieved(str(byte))
    waitTillnRecieved("done")
