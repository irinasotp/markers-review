# import the necessary packages
import apriltag
import argparse
import cv2
import os
from timeit import default_timer as timer

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--string", type=str,
	default="apriltag", help="string in name of images")
ap.add_argument("-i", "--image", type=str,
	default="", help="image path")
args = vars(ap.parse_args())

#global variables
nrTagsDetected = 0
nrFiles = 0
deltaTime = 0
totalTime = 0

def detect_april_markers(f):
	global nrFiles
	global nrTagsDetected
	global deltaTime
	global totalTime

	nrFiles += 1
	print("\n")

	# load the input image from disk and resize it
	print("[INFO] loading image...{}".format(f))
	image = cv2.imread(f)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.blur(gray, (2,2))

	# define the AprilTags detector options and then detect the AprilTags
	# in the input image
	print("[INFO] detecting AprilTags...")
	options = apriltag.DetectorOptions(families="tag36h11")
	detector = apriltag.Detector(options)

	start = timer()
	results = detector.detect(gray)
	deltaTime = timer() - start
	totalTime += deltaTime
	print("[INFO] Detection in {} seconds ".format(deltaTime))

	print("[INFO] {} total AprilTags detected".format(len(results)))

	# loop over the AprilTag detection results
	for r in results:
		tagFamily = r.tag_family.decode("utf-8")
		if (tagFamily == 'tag36h11' and r.tag_id == 10):
			nrTagsDetected += 1

def iterate_over_files(directory):
	if args["image"]: # if is not empty
		detect_april_markers(args["image"])
	else:
		for filename in os.listdir(directory):
			f = os.path.join(directory, filename)

			# checking if it is a file
			if os.path.isfile(f) and args["string"] in filename:
				detect_april_markers(f)
			elif not os.path.isfile(f): # means is a directory
				iterate_over_files(f)


def performance_test():
	for i in range(10):
		if args["image"]: # if is not empty
			detect_april_markers(args["image"])

	

# assign directory
directory = '/home/irina/Documents/dataset_apriltag_aruco_cctag/spin/apriltag_images'
iterate_over_files(directory)
#performance_test()

print("  ")
print("==============================")
print("  ")
print("[Result] Tags detected: {}".format(nrTagsDetected))
print("[Result] Files as input: {}".format(nrFiles))
print("[Result] Rate of detection: {}%".format(nrTagsDetected/nrFiles * 100))
print("[Result] Total detection in {}".format(totalTime))
print("[Result] Average time per image is {} seconds".format(totalTime/nrFiles))
print("  ")
print("---------------------------------------------------------")
print("  ")