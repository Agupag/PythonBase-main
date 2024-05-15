import socket
import netifaces as ni
from tkinter import *
from tkinter import ttk
import tkinter as tk
from Drone import Drone
from threading import Thread
from queue import Queue
from pynput.keyboard import Key, Listener
import time
#pip3 install "requests>=2.*"
#pip3 install netifaces
global UDP_IP
UDP_IP = 0
def getMyIP():
    try:
        hostname = socket.gethostname()
        print(hostname)
        print("00000")
        # ipv4_address = socket.gethostbyname(hostname + ".local")
        # print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")
        # 
        ip = ni.ifaddresses('en1')[ni.AF_INET][0]['addr']
        UDP_IP = ip
        UDP_PORT = 5005
        print(ip)
    except socket.gaierror as e:
        print("There was an error resolving the hostname.")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

getMyIP()
#ip = ni.ifaddresses('en1')[ni.AF_INET][0]['addr']
 #ask mclain how to do this on windows
#UDP_IP = ip
UDP_IP = "192.168.1.54"
UDP_PORT = 5005

#BRENDAN CODE _____________________________________________________________________________________________________
global yaw, roll, pitch, throttle, keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, shouldQuit
yaw = 0
keyQ = False
keyE = False
roll = 0 
keyA = False
keyD = False
pitch = 0
keyW = False
keyS = False
throttle = 0
keyAU = False
keyAD = False
shouldQuit = False
global selDrone
global selDroneTK




def clamp(val):
    lowLimit = -100
    highLimit = 100
    if val < lowLimit:
        val = lowLimit
    if val > highLimit:
        val = highLimit   
    return val
def introToAP():
    #tell the AP that we are the base station. 
    #AP needs to save that IP address to tell it to drones (so they can connect to the base station)
    pass
def show(key):
    global yaw, roll, pitch, throttle, keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, shouldQuit
    if key == Key.up:
        keyAU = True
        return
    if key == Key.down:
        keyAD = True
        return
    if key.char == 'q':
        keyQ = True
    if key.char == 'e':
        keyE = True
    if key.char == 'a':
        keyA = True
    if key.char == 'd':
        keyD = True
    if key.char == 'w':
        keyW = True
    if key.char == 's':
        keyS = True
    if key.char == 'p':
        shouldQuit = True
def release(key):
    global keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, throttle
    if key == Key.up:
        keyAU = False
        return
    if key == Key.down:
        keyAD = False
        return
    if key.char == 'q':
        keyQ = False   
    if key.char == 'e':
        keyE = False
    if key.char == 'a':
        keyA = False
    if key.char == 'd':
        keyD = False
    if key.char == 'w':
        keyW = False
    if key.char == 's':
        keyS = False
# Collect all event until released
#BRENDAN CODE _____________________________________________________________________________________________________

def handshake(msg, addr):
    
    parts = msg.split("|")
    i = int(parts[1])
   
    if (i == -1):
        i = len(drones)
        print(i)
        print(addr)
        print(addr[1])
        drone =  Drone(i, parts[2], addr[0], addr[1])
        drones.append(drone)
        for adrone in drones:
            print(adrone)
        updateList()
        #sendMessage(drone.ipAddress, drone.port, "HSC|" + str(i))

    else:
        if drones[i].name == parts[2]:
            #we could update here
            drones[i].ipAddress = addr[0]
            drones[i].port = addr[1]
    droneList.update()    
def sendMessage(ipAddress, port, msg):
    print("sendMessage")
    print(ipAddress)
    print(port)
    print(msg)
    print("----------------------------")    
    bMsg = msg.encode("ascii")
    sendSocket.sendto(bMsg, (ipAddress, int(port)))
    print("sent message")
def manualControl():
    listener =  Listener(on_press = show, on_release = release)   
    listener.start()
    global yaw, roll, pitch, throttle, keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, shouldQuit
    # yaw = 0
    # keyQ = False
    # keyE = False
    # roll = 0 
    # keyA = False
    # keyD = False
    # pitch = 0
    # keyW = False
    # keyS = False
    # throttle = 0
    # keyAU = False
    # keyAD = False
    # shouldQuit = False
    while True:
        if keyQ:
            yaw -= 0.01
        elif keyE:
            yaw += 0.01
        if keyA:
            roll -= 0.01
        elif keyD:
            roll += 0.01
        if keyW:
            pitch += 0.01
        elif keyS:
            pitch -= 0.01
        if keyAU:
            throttle += 0.01
        elif keyAD:
            throttle -= 0.01
        if shouldQuit:
            listener.stop()
            break



        if yaw > 0 and keyQ == False and keyE == False:
            yaw -= 0.01
        elif yaw < 0 and keyQ == False and keyE == False:
            yaw += 0.01
        if roll > 0 and keyA == False and keyD == False:
            roll -= 0.01
        elif roll < 0 and keyA == False and keyD == False:
            roll += 0.01
        if pitch > 0 and keyW == False and keyS == False:
            pitch -= 0.01
        elif pitch < 0 and keyW == False and keyS == False:
            pitch += 0.01
        if throttle > 0 and keyAU == False and keyAD == False:
            throttle -= 0.01
        elif throttle < 0 and keyAU == False and keyAD == False:
            throttle += 0.01

        
        yaw = clamp(yaw)
        roll = clamp(roll)
        pitch = clamp(pitch)
        throttle = clamp(throttle)
        yaw = round(yaw, 2)
        roll = round(roll, 2)
        pitch = round(pitch, 2)
        throttle = round(throttle, 2)
        # print(yaw, " -- yaw")
        # print(roll, " -- roll")
        # print(pitch, " -- pitch")
        # print(throttle, " -- throttle")
        for i in droneList.curselection():
            selDrone = drones[i]
            print(selDrone)
        
        #print(selDrone.ipAddress)
        #sendMessage(selDrone.ipAddress, selDrone.port, "|" + str(yaw) + "|" + str(roll) + "|" + str(pitch) + "|" + str(throttle) + "|")
        #print(yaw)
        #sendMessage(selDrone.ipAddress, selDrone.port, yaw + str(i))

        
        time.sleep(0.01)

def updateList():
    #clear the list box
    droneList.delete(0, len(drones)-1)

    #walk through drones
    for i in range(len(drones)):
        droneList.insert(i, str(drones[i]))
    #insert all the drone elements


def listDrones():
    global drones
    for drone in drones:
        print(drone.name, drone.ipAddress, drone.port, "\t") 

def listen(q_out, q_in):#happens on a separate thread
    
    while True:
        #check if we need to stop--grab from q_in  
        data = b""    #the b prefix makes it byte data
        if (not q_in.empty()):
            qIn = q_in.get()
            if (qIn == "TERMINATE"):
                q_out.put("STOPPING")
                break
        try:
            data, addr = sock.recvfrom(1024)
        except:
            continue
        strData = data.decode("utf-8")
        print("Received message %s" % data)
        # strData = strData + "|" + addr[0] + "|" + str(addr[1])#the message, the ip, the port
        strData = addr[0] + "*" + str(addr[1]) + "*" + strData#the ip, the port, the message
        # the message is pipe (|) delimited. The ip, port, and message are * delimited
        q_out.put(strData) #this sends the message to the main thread
        # parts = strData.split("|")
        # print(parts)
        # cmd = parts[0]

        # if cmd == "HND":
        #     #HANDSHAKE
        #     handshake(parts, addr)
    print("goodbye")
def addDrone():
    #this is just to test if tkinter will add them to the listbox on a button press.
    drones.append(Drone(8, "test", "none", 17))
    print(str(drones))
def checkQueue(q_in):
    selDroneTK.set(selDrone.ipAddress)
    root.update_idletasks()
    #print(selDrone.ipAddress)
    if (not q_in.empty()):
        print("checking queue")
        #grab the item
        #process the info
        #mark it complete
        data = q_in.get()
        parts = data.split("*")
        addr = parts[0]
        port = int(parts[1])
        msg = parts[2]
        # print(parts)
        msgParts = msg.split("|")

        cmd = msgParts[0]

        if cmd == "HND":
            #HANDSHAKE
            handshake(msg, (addr, port))
    root.after(1000, checkQueue, q_in)


#--------------------------------------------
#------------    Main Code ------------------

qFromComms = Queue() #gets information from the comms thread
qToComms = Queue() #sends information to the comms thread
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

terminate = False
maxDrones = 3
drones = []
#these next two lines are for testing only. Remove them
drones.append(Drone(0, "one", "10.20.18.23", 85))
drones.append(Drone(1, "two", "10.20.18.23", 85))
drones.append(Drone(2, "three", "192.168.4.22", 80))
selDrone = drones[0]

#----- Setup our GUI --------
root = Tk()
root.geometry("400x400")
root.title("Drone Manager")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="hello world").grid(column = 0, row = 0)
ttk.Label(frm, text="Drones List").grid(column = 0, row = 1)

listVar = StringVar(value = drones)
droneList = Listbox(master = root,width =10, height = 25, listvariable = listVar)

droneList.grid(column = 0, row = 2)
black = "black"

selDroneTK = tk.StringVar(root)

ttk.Label(root, text="Name | IP | Port").grid(column = 2, row = 1,padx=50)
ttk.Label(root, textvariable=selDroneTK).grid(column = 2, row = 2,padx=50)


#--------- END OF FIRST GRAB ----------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))

print("Ready3")
#----- END OF SECOND GRAB

#-----------  WHAT WAS ALREADY HERE IS BELOW
t = Thread(target=listen, args=(qFromComms, qToComms))
t.start()
m = Thread(target=manualControl, args=())
m.start()
root.after(1000, checkQueue, qFromComms)
# root.bind("<<updateevent>>", updateDronesList)
root.mainloop()
qToComms.put("TERMINATE") #tell the subloop on the backup thread to quit.
t = qFromComms.get(timeout=3.0)
#give it a chance to quit
print("all done")
exit(0)



