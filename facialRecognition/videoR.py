from imutils import paths
import argparse
import pickle
import os
import numpy
import cv2
import face_recognition
def changeRes(width,height):
	# this is a method i will use on the live video
	capture.set(3,width)
	capture.set(4, height)

# will use this for later
def rescaleFrame(frame, scale=.75):
	width = int(frame.shape[1]*scale)
	height= int(frame.shape[0]*scale)
	dimensions=(width.height)
	return cv.resize(frame,dimension,interpolation=cv.INTER_AREA)




ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
                help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
                help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))


knownEncodings = []
knownNumbers = []

while True:
	frame = vs.read()

	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=750)
	r = frame.shape[1] / float(rgb.shape[1])

	boxes = face_recognition.face_locations(rgb,
											model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []


for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]


	image = cv2.imread(imagePath)
	image = cv2.resize(image,(300,300))
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	encodings = face_recognition.face_encodings(rgb, boxes)

	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)

print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
