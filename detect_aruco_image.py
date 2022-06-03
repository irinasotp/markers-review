# import the necessary packages
import argparse
import imutils
import cv2
import sys
import os
from timeit import default_timer as timer

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_6X6_50",
	help="type of ArUCo tag to detect")
ap.add_argument("-s", "--string", type=str,
	default="aruco", help="string in name of images")
args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

#global variables
nrTagsDetected = 0
nrWrongTags = 0
nrFiles = 0
deltaTime = 0
totalTime = 0

def detect_aruco_markers(f):
	global nrFiles
	global nrTagsDetected
	global deltaTime
	global totalTime

	nrFiles += 1
	print("\n")

	# load the input image from disk and resize it
	print("[INFO] loading image...{}".format(f))
	image = cv2.imread(f)
	image = imutils.resize(image, width=600)

	# verify that the supplied ArUCo tag exists and is supported by
	# OpenCV
	if ARUCO_DICT.get(args["type"], None) is None:
		print("[INFO] ArUCo tag of '{}' is not supported".format(
			args["type"]))
		sys.exit(0)

	# load the ArUCo dictionary, grab the ArUCo parameters, and detect
	# the markers
	print("[INFO] detecting '{}' tags... ".format(args["type"]))
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
	arucoParams = cv2.aruco.DetectorParameters_create()

	# detection phaze
	start = timer()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
		parameters=arucoParams)
	deltaTime = timer() - start
	totalTime += deltaTime
	print("[INFO] Detection in {} seconds ".format(deltaTime))

	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()
		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			print("[INFO] ArUco marker ID: {}".format(markerID))
			if (markerID == 10):
				nrTagsDetected += 1
			else:
				nrWrongTags += 1
	
def iterate_over_files(directory):
	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)

		# checking if it is a file
		if os.path.isfile(f) and args["string"] in filename:
			detect_aruco_markers(f)
		elif not os.path.isfile(f): # means is a directory
			iterate_over_files(f)

# assign directory
directory = '/home/irina/Documents/dataset_apriltag_aruco_cctag/spin/aruco_images'
iterate_over_files(directory)

print("  ")
print("==============================")
print("  ")
print("[Result] Tags detected: {}".format(nrTagsDetected))
print("[Result] Files as input: {}".format(nrFiles))
print("[Result] Rate of detection: {}%".format(nrTagsDetected/nrFiles * 100))

print("  ")
print("[False positive] Nr of wrong tags: {}".format(nrWrongTags))
print("[False positive] False positive rate: {}".format(nrWrongTags/nrFiles * 100))
print("  ")

print("[Result] Total detection in {}".format(totalTime))
print("[Result] Average time per image is {} seconds".format(totalTime/nrFiles))
print("  ")
print("---------------------------------------------------------")
print("  ")


