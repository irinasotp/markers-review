import numpy as np
import cv2
import time
import baslercamera
import threading
import sys
from PIL import Image
import servo as srv

FRAME_NUMBER = 20

def thread_function(time):
    srv.stopFlag = False
    srv.spin_exe(time)


def varianta(direction, spin):
    global angle_name

    if spin == False:
        if direction == "left":
            srv.set("yaw", 1800)
        elif direction == "right":
            srv.set("yaw",1200)

        angle_name = direction
    else:
        angle_name = "spin_180"

cap = baslercamera.BaslerVideoCapture()

def get_frame(namePhoto, exposure):
    cap.set_gain_exp_time(exposure, 0)

    for i in range(0, FRAME_NUMBER):
        frame = cap.read()
        
        # Display the resulting frame
        #cv2.imshow('frame', frame)
        
        data = Image.fromarray(frame)

        # compute the name of the photos
        if i < 10:
            namePhoto = namePhoto + "0"
        namePhoto = namePhoto + str(i) + ".png"

        # save photo
        data.save(namePhoto, format="png")

def get_marker_frame(timeList, exposureList, namePhoto,spin):
    if spin:
        for time in timeList:
            print("\nTime delay: " + str(time))
            thread1 = threading.Thread(target=thread_function, args=(time,))
            thread1.start()
            print ("Start thread")

            for exposure in exposureList:
                print("\tExposure: " + str(exposure))
                namePhoto = namePhoto + str(exposure) + "_"
                get_frame(namePhoto, exposure)

            srv.stopFlag = True
            print("Stop thread")
            thread1.join()
    else:
        for exposure in exposureList:
            print("\tExposure: " + str(exposure))
            namePhoto = namePhoto + str(exposure) + "_"
            get_frame(namePhoto, exposure)

def readKey(message, waitingInput):
    print(message)
    for line in sys.stdin:
        if waitingInput == line.rstrip():
            break
        print("You must type " + waitingInput)

def turnTheLight(condition):
    if condition:
        return "_light_"
    else:
        return "_dark_"


timeList = [0.001505, 0.001125, 0.00075, 0.0005, 0.000375] # 45, 60, 90, 135, 180 degree/sec
distanceList = [50, 100, 150, 200, 250] # distances in cm
exposureList = [1000, 3000, 7000, 10000, 12000, 15000, 18000]
markerList = ["aruco", "apriltag", "cctag"]

# distance between camera and marker
distance = int(input("Please introduce the distance: "))
step = 0 # help us for light condition switch
spin = True # tell us about servo, if it spins or not
srv.init_servo()
varianta("center", spin) # set servo taking into account the direction; 

for marker in markerList:
    condition = step % 2 == 0
    namePhoto = "./" + marker + "_images/" + marker + "_" + angle_name + "_" + str(distance)

    print ("\nNext marker: " + marker + "\nDistance: " + str(distance) + " cm" + "\nIlluminate conditions: " + turnTheLight(condition))

    # asteapta input de la user
    readKey("\nWould you like to continue ? [y/n]", 'y')

    # facem poze la toate vitezele si toate exposures
    # pentru un marker in conditie de lumina aprinsa/stinsa
    get_marker_frame(timeList, exposureList, namePhoto + turnTheLight(condition), spin)

    # asteapta input de la user
    readKey("Please turn the light! Press 'd' after that", 'd')

    # poze pentru marker cu lumina stinsa/aprinsa (opus apelarii de mai sus)
    get_marker_frame(timeList, exposureList, namePhoto + turnTheLight(not condition), spin)

    step += 1

srv.stop_servo()

# When everything done, release the capture
cv2.destroyAllWindows()
