import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
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
                    print("RFID ID: %s\nUser Id: %s\nUser Name: %s\n" % (id,dlist[0],dlist[1]))
                else:
                    print(text)
                time.sleep(1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise

read_data()
