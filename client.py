from socket import *
import datetime
import os
serverName = '127.0.0.1'
serverPort = 11000

def title_bar():
    os.system('clear')
    print("\t**********************************************")
    print("\t***** RFID Model Detection *****")
    print("\t**********************************************")


def mainMenu():
    title_bar()
    print()
    print(10 * "*", "WELCOME MENU", 10 * "*")
    print("[1] Add New User")
    print("[2] Read/Detect User")
    print("[3] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                # CaptureFaces()
                choice_id = (str(choice)+",").encode()
                Id = input('Enter your Id: ').encode()
                Name = input('Enter your Name: ')
                Namewith = (","+Name).encode()
                #AF_INET is for IPv4 - SOCK_STREAM is for TCP
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverName,serverPort))
                clientSocket.send(choice_id)
                clientSocket.send(Id)
                clientSocket.send(Namewith)
                print ('<-- message sent to server',clientSocket.getpeername()[0],":",clientSocket.getpeername()[1],'on', datetime.datetime.now())
                print(clientSocket.recv(1024).decode("utf-8"))
                print ('-----------------------------------------------------')
                clientSocket.close()
                print ('TCP connection with server is closed')
                # ----------------------------------------------------------------------------
                mainMenu()
                break
            
            elif choice == 2:
                print("Read/Detect User")
                choice_id = (str(choice)+",").encode()

                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverName,serverPort))
                clientSocket.send(choice_id)

                mainMenu()
                break
            
            elif choice == 3:
                print("Thank You")
                break
            else:
                print("Invalid Choice. Enter 1-3")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-3\n Try Again")
    exit

mainMenu()
