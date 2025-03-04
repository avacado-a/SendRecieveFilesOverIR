import time
import subprocess
try:
    subprocess.Popen(['python', "SandySerial.py"])
    print(f"Started running SandySerial.py in the background.")
except FileNotFoundError:
    print(f"Error: Could not find SandySerial.py.")
except Exception as e:
    print(f"An error occurred while running SandySerial.py: {e}")
file = open("liveDrawComms.txt","w")
file.write("0,0")
file.close()
def addPosition(angle:int,distance:int, offset:int=0):
    """
    Adds a position to the "liveDrawComms.txt" file based on the given angle, distance, and optional offset.

    Args:
        angle (int): The angle in degrees.
        distance (int): The distance value.
        offset (int, optional): The offset to be added to the angle. Defaults to 0.

    Returns:
        bool: True if the position was successfully added, False otherwise.

    Raises:
        BaseException: If an error occurs while reading or writing to the file.
    """
    angle+=offset
    angle=360-angle
    angle=angle%360
    try:
        file = open("liveDrawComms.txt","r")
        a = file.read().split("\n")
        b = a[len(a)-1].split(",")
        file.close()
        file = open("liveDrawComms.txt","a")
        if len(b)==0:
            file.write(str(angle)+","+str(distance))
            file.close()
            return True
        else:
            file.write("\n"+str(angle)+","+str(distance))
            file.close()
            return True
    except BaseException as e:
        print(f"An error occurred while adding position: {e}")
        return False
def readPosition():
    """
    Reads the last position from the "liveDrawComms.txt" file.

    The function attempts to open the "liveDrawComms.txt" file in read mode,
    reads its contents, and splits the last line by a comma to extract the
    position coordinates. If successful, it returns the coordinates as a tuple
    of two integers. If an error occurs during this process, it prints an error
    message and returns (-1, -1).

    Returns:
        tuple: A tuple containing two integers representing the position 
               coordinates. Returns (-1, -1) if an error occurs.
    """
    try:
        file = open("liveDrawComms.txt","r")
        a = file.read().split("\n")
        b = a[len(a)-1].split(",")
        file.close()
        return (int(b[0]),int(b[1]))
    except BaseException as e:
        print(f"An error occurred while reading position: {e}")
        return (-1,-1)
def clearAllPositions():
    """
    Clears all positions by writing an empty string to the file 'liveDrawComms.txt'.

    This function attempts to open the file 'liveDrawComms.txt' in write mode and 
    clears its contents. If an error occurs during this process, it catches the 
    exception, prints an error message, and returns None.

    Returns:
        bool: True if the file was successfully cleared, otherwise None.
    """
    try:
        file = open("liveDrawComms.txt","w")
        file.write("")
        file.close()
        return True
    except BaseException as e:
        print(f"An error occurred while clearing all positions: {e}")
        return

# The code above this comment should not be touched. It is base functions you can use in your code. 
# You are given two functions to use in your code: addPosition and readPosition.
# Below is an example simple clock that updates every 10 minutes. Delete it and write your own code.

from datetime import datetime
def clearBoard():
    """
    Clears the board by generating a series of instructions to add positions in a spiral pattern.

    The function creates a list of instructions where each instruction is a tuple containing an angle and a distance.
    The angles are generated in increments of 5 degrees, and the distances decrease from 75 to 0 in steps of 15.
    The angle alternates between clockwise and counterclockwise for each distance step.

    The generated instructions are then used to call the addPosition function with the respective angle and distance.

    Returns:
        None
    """
    instructions = []
    flip = False
    for distance in range(75,0,-15):
        for angle in range(0,360,5):
            instructions.append((360-angle if flip else angle,distance))
        flip = not flip
    for i in instructions:  
        addPosition(i[0],i[1])
addPosition(0,60)
addPosition(0,60)
red = (0,60)
while red == (0,60):
    red = readPosition()
    time.sleep(0.05)
inp = 0
print("Enter a number between 0 and 360 for the 12 hand on the clock. Type 'exit' to exit.")
while inp != "exit":
    try:
        inh = input(">")
        if inh == "exit":
            break
        inp = int(inh)
    except:
        print("Invalid input. Please enter a number between 0 and 360 for the 12 hand on the clock. Type 'exit' to exit.")
        continue
    if inp < 360 and inp > 0:
        addPosition(inp,60)
clearBoard()
addPosition(0,0,inp)
now = datetime.now()
lastMin=-1
addPosition((now.hour%12)*30,0,inp)
addPosition((now.hour%12)*30,40,inp)
addPosition((now.hour%12)*30,0,inp)
addPosition((now.minute//10)*10*6,0,inp)
addPosition((now.minute//10)*10*6,80,inp)
addPosition((now.minute//10)*10*6,0,inp)
addPosition(0,0,inp)
while True:
    now = datetime.now()
    if now.minute%10 == 0 and now.minute != lastMin:
        clearBoard()
        addPosition((now.hour%12)*30,0,inp)
        addPosition((now.hour%12)*30,40,inp)
        addPosition((now.hour%12)*30,0,inp)
        addPosition((now.minute//10)*10*6,0,inp)
        addPosition((now.minute//10)*10*6,80,inp)
        addPosition((now.minute//10)*10*6,0,inp)
        addPosition(0,0,inp)
        lastMin = now.minute