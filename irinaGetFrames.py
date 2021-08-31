import numpy as np
import cv2
import time
import baslercamera
import threading
import sys
from PIL import Image
import servo as srv

def thread_function(time):
    srv.stopFlag = False
    srv.swing_exe(time)


def varianta(marker, dir, dist, servo, et, g, cond):
    global marker_name
    global angle_name
    global distance
    global exp_time
    global gain
    global condition

    if servo == True:
        srv.init()
        if dir == "left":
            srv.set("yaw", 1800)
        elif dir == "center":
            srv.set("yaw",1500)
        elif dir == "right":
            srv.set("yaw",1200)

        srv.set("pitch", 1500)
        angle_name = dir
    else:
        angle_name = "swing_180"

    marker_name = marker
    distance = dist
    exp_time = et
    gain = g
    condition = cond
    
    

cap = baslercamera.BaslerVideoCapture()
cap.calibrate_time()

def get_frame(exposure, marker, lightCondition, distance):

    #varianta(marker, "center", distance, False, exposure, 0, lightCondition)
    varianta(marker, "center", distance, False, exposure, 0, lightCondition)

    cap.set_gain_exp_time(exp_time, gain)

    frame_number = 20

    i = 0
    while(i < frame_number):
        rez, frame, fr_time = cap.read()
        
        # Display the resulting frame
        #cv2.imshow('frame', frame)
        
        data = Image.fromarray(frame)
        i = i+1

        if i < 10:
            data.save("./" + marker_name + "_" + "images" + "/" + marker_name + "_" + angle_name + "_" + str(distance) + "_" + str(exp_time) + "_" + str(gain) + "_" + condition + "_0" + str(i) + ".png", format="png")
        else:
            data.save("./" + marker_name + "_" + "images" + "/" + marker_name + "_" + angle_name + "_" + str(distance) + "_"  + str(exp_time) + "_" + str(gain) + "_" + condition + "_" + str(i) + ".png", format="png")

def get_marker_frame(marker, timeList, exposureList, lightCondition, distance):
    for time in timeList:
        print("\nTime delay: " + str(time))
        thread1 = threading.Thread(target=thread_function, args=(time,))
        thread1.start()
        print ("Start thread")

        for exposure in exposureList:
            print("\tExposure: " + str(exposure))
            get_frame(exposure, marker, lightCondition, distance)

        srv.stopFlag = True
        print("Stop thread")
        thread1.join()

def readKey(message, waitingInput):
    print(message)
    for line in sys.stdin:
        if waitingInput == line.rstrip():
            break
        print("You must type " + waitingInput)

def turnTheLight(condition):
    if condition:
        return "light"
    else:
        return "dark"


timeList = [0.001505, 0.001125, 0.00075, 0.0005, 0.000375] # 45, 60, 90, 135, 180 degree/sec
distanceList = [50, 100, 150, 200, 250] # distante masurate in cm
exposureList = [1000, 3000, 7000, 10000, 12000, 15000, 18000]
markerList = ["aruco", "apriltag", "cctag"]

distance = int(input("Please introduce the distance: "))

step = 0
for marker in markerList:
    condition = step % 2 == 0

    print ("\nNext marker: " + marker + "\nDistance: " + str(distance) + " cm" + "\nIlluminate conditions: " + turnTheLight(condition))

    # asteapta input de la user
    readKey("\nWould you like to continue ?", 'y')

    # facem poze la toate vitezele si toate exposures
    # pentru un marker in conditie de lumina aprinsa
    get_marker_frame(marker, timeList, exposureList, turnTheLight(condition), distance)

    # asteapta input de la user
    readKey("Please turn the light!", 'd')

    # poze pentru marke cu lumina stinsa
    get_marker_frame(marker, timeList, exposureList, turnTheLight(not condition), distance)

    step += 1



# When everything done, release the capture
cv2.destroyAllWindows()
