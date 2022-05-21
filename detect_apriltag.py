# import the necessary packages
import apriltag
import argparse
import cv2
import os

#global variables
nrTagsDetected = 0
nrFiles = 0

# assign directory
directory = 'dataset_apriltag_aruco_cctag/spin/apriltag_images/150'

#iterate over files in that directory
for filename in os.listdir(directory):
	f = os.path.join(directory, filename)

	# checking if it is a file
	if os.path.isfile(f):
		nrFiles += 1
		print("\n")
		print(f)

		# load every image and convert it to grayscale
		print("[INFO] loading image...")
		image = cv2.imread(f)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.blur(gray, (2,2))

		# define the AprilTags detector options and then detect the AprilTags
		# in the input image
		print("[INFO] detecting AprilTags...")
		options = apriltag.DetectorOptions(families="tag36h11")
		detector = apriltag.Detector(options)
		results = detector.detect(gray)
		print("[INFO] {} total AprilTags detected".format(len(results)))

		# loop over the AprilTag detection results
		for r in results:
			tagFamily = r.tag_family.decode("utf-8")
			if (tagFamily == 'tag36h11' and r.tag_id == 10):
				nrTagsDetected += 1

print("------------------------------")
print("[Result] Tags detected: {}".format(nrTagsDetected))
print("[Result] Files as input: {}".format(nrFiles))
print("[Result] Rate of detection: {}%".format(nrTagsDetected/nrFiles * 100))