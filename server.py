from socket import *
import datetime
import time
import os
import os.path
from os import error, path
import sys

from threading import Thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

#to count the number of clients connected to our server
clientCount = 1
serverPort = 11000
#AF_INET is for IPv4 - SOCK_STREAM is for TCP
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is listening on localhost :', serverPort)
print ('-----------------------------------------------------')
lst = []
global stop_threads
stop_threads = False
reader = SimpleMFRC522()
def read_data():
    try:
        while True:
            print("status: ",stop_threads)
            if stop_threads:
                break
            else:
                print("Hold a tag near the reader")
                id, text = reader.read()
                dlist = text.split(",")
                if len(dlist) > 1:
                    print("RFID ID: %s\nUser Id: %s\nUser Name: %s\nPunch Time: %s\n" % (id,dlist[0],dlist[1],str(datetime.datetime.now())))
                else:
                    print(text)
                time.sleep(1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise

while 1:
    if len(lst) == 0:
        print("list is empty")
        stop_threads = False
        t = Thread(target = read_data)
        t.start()

    connectionSocket, addr = serverSocket.accept()
    lst.append(connectionSocket.getpeername()[0])
    if len(lst) == 0:
        print("list is empty")
    else:
        print("Listr is not empty")

    print ('Client #', clientCount)
    # print ('--> message reveived from client #', clientCount,connectionSocket.getpeername()[0],":",connectionSocket.getpeername()[1],'on', datetime.datetime.now())
    
    data = connectionSocket.recv(1024).decode("utf-8")
    print("Data : ",data)
    datalst  = data.split(",")
    print(datalst)
    choice = int(datalst[0])
    if choice == 1:
        stop_threads = True
        t.join()
        Id = datalst[1]
        Name = datalst[2]
        print(len(Name)," And ",len(Id))
        
        if len(Name) > 0 or len(Id) > 0:
            dlt = Id+","+Name
            print("Name:",dlt)
            # reader = SimpleMFRC522()
            try:
                    print("Now place your tag to write")
                    reader.write(dlt)
                    print("Written Done..")
            finally:
                    GPIO.cleanup()  

        connectionSocket.send("Please Wait...".encode())

    elif choice == 2:
        print("Process..")
        stop_threads = False
        t = Thread(target = read_data)
        t.start()
        connectionSocket.send("Please Wait...".encode())
        
    else:
        print("Something Wrong..")
        break
    # print(connectionSocket.recv(1024).decode("utf-8"))
    connectionSocket.close()
    print ('Connection closed with User #', clientCount)
    print ('-----------------------------------------------------')
    clientCount += 1 
