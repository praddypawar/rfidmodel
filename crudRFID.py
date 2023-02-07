import os
from textwrap import indent
from threading import Thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
import time
import datetime

reader = SimpleMFRC522()

# print(reader.read(),"----")

# idd,text = reader.read()
# dlt = """ sdfdsfsdfdfdsfsddssd dsdfsdfsdfsdf fgsdhfgsdhgf fdfdfg gdfhgjdfhg fdg"""
# print(len(dlt))
# time.sleep(1)
# reader.write(dlt)
# iddd = reader.read()
# print(iddd)

def adduser(reader_id,name,email):
    with open("userList.json","r") as addata:
        userlist = json.load(addata)
    if len(userlist) == 0:
        uid =1
    else:
        uid = int(userlist[-1]["id"])+1
    d1 = {
            "id":uid,
            "reader_id":reader_id,
            "name":name,
            "email":email,
            "date":str(datetime.datetime.now())
        }
    userlist.append(d1)
    # with open("userList.json","w") as addata:
    #     json.dump(userlist,addata,indent=4)
    return [d1,userlist]

def updateuser(uid,name,email):
    with open("userList.json","r") as addata:
        userlist = json.load(addata)

    for j in range(len(userlist)):
        if userlist[j]["id"]==uid:
            userlist[j]["name"]=name
            userlist[j]["email"]=email
            userlist[j]["date"]=str(datetime.datetime.now())
            
        with open("userList.json","w") as addata:
            json.dump(userlist,addata,indent=4)
        return userlist[j]

def deleteuser(uid):
    with open("userList.json","r") as addata:
        userlist = json.load(addata)
    try:
        for j in range(len(userlist)):
            if userlist[j]["id"]==uid:
                del userlist[j]
                break
                
        with open("userList.json","w") as addata:
            json.dump(userlist,addata,indent=4)
        return True
    except Exception as e:
        return False

    



while True:
    print("---------- Menu -----------")
    print("1. Add New User")
    print("2. Update User")
    print("3. Delete User")
    print("4. List Out User")
    print("5. Actual tag Detail")
    print("6. Exit")
    choice = int(input("Enter Choice: "))
    if choice == 1:
        print("1. Add New User")
        print("Hold a tag near the reader")
        reader_id,text = reader.read()
        
        with open("userList.json","r") as addata:
            userlist = json.load(addata)
        for i in userlist:
            try:
                if i["id"] == int(text):
                    print("tag already used.")
                    break
            except Exception:
                pass
        else:
            name = input("Enter Your name: ")
            email = input("Enter Your email: ")
            
            d1 = adduser(reader_id,name,email)
            print("Now place your tag to write")
            w_data = reader.write(str(d1[0]["id"]))
            if len(w_data) == 2:
                with open("userList.json","w") as addata:
                    json.dump(d1[1],addata,indent=4)
            # print("-=-=-=-=-=-")
            print("Data added.\n",d1[0])
    #---------------------------------------------------------------
    elif choice == 2:
        print("2. Update User")
        uid = int(input("ID: "))
        with open("userList.json","r") as addata:
            userlist = json.load(addata)
        for i in userlist:
            if i["id"] != uid:
                print("ID data not exist.")
                break
                
        else:
            name = input("Enter Your name: ")
            email = input("Enter Your email: ")
            d1 = updateuser(uid,name,email)
            print("Data updates\n",d1)
        
    #---------------------------------------------------------------
    elif choice == 3:
        print("3. Delete User")
        print("Hold a tag near the reader")
        reader_id,text = reader.read()

        with open("userList.json","r") as addata:
            userlist = json.load(addata)
        for i in userlist:
            try:
                if i["id"] == int(text):
                    print("tag founded.")
                    res = deleteuser(i["id"])
                    if res:
                        w_data = reader.write("0")
                        print("Tag removed.")
                    break
            except Exception:
                pass

    #---------------------------------------------------------------
    elif choice == 4:
        print("4. List Out User")
        with open("userList.json","r") as addata:
            userlist = json.load(addata)
        print(userlist)
    #---------------------------------------------------------------
    elif choice == 5:
        data = reader.read()
        print(data)

    elif choice == 6:
        break
