from imutils import paths
import argparse
import pickle
import os
import numpy as np
import cv2

image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("in_memory_to_disk.png", image)
pyautogui.screenshot("straight_to_disk.png")
image = cv2.imread("straight_to_disk.png")
cv2.imshow("Screenshot", imutils.resize(image, width=600))
cv2.waitKey(0)