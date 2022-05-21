# import the necessary packages
import argparse
import imutils
import cv2
import sys
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_APRILTAG_36h11",
	help="type of ArUCo tag to detect")
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
nrFiles = 0

# assign directory
directory = 'dataset_apriltag_aruco_cctag/no_spin/apriltag_images'

#iterate over files in that directory
for filename in os.listdir(directory):
	f = os.path.join(directory, filename)

	# checking if it is a file
	if os.path.isfile(f):
		nrFiles += 1
		print("\n")
		print(f)

		# load the input image from disk and resize it
		print("[INFO] loading image...")
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
		print("[INFO] detecting '{}' tags...".format(args["type"]))
		arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
		arucoParams = cv2.aruco.DetectorParameters_create()
		(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
			parameters=arucoParams)

		# verify *at least* one ArUco marker was detected
		if len(corners) > 0:
			# flatten the ArUco IDs list
			ids = ids.flatten()
			# loop over the detected ArUCo corners
			for (markerCorner, markerID) in zip(corners, ids):
				print("[INFO] ArUco marker ID: {}".format(markerID))
				if (markerID == 10):
					nrTagsDetected += 1

print("------------------------------")
print("[Result] Tags detected: {}".format(nrTagsDetected))
print("[Result] Files as input: {}".format(nrFiles))
print("[Result] Rate of detection: {}%".format(nrTagsDetected/nrFiles * 100))


