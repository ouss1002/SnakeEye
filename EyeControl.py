import cv2
from mtcnn.mtcnn import MTCNN
import win32api, win32con, win32gui
import math
import pyautogui

pyautogui.FAILSAFE = False

def doubleclick():
    pyautogui.click()
    pyautogui.click()

def isclosed(img, eye):
	gray = img[eye[1], eye[0]]

	return gray > 100

def click(x, y):
    win32api.SetCursorPos((x, y))
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def move(x, y, coeff = 1):
	flags, hcursor, (pos1, pos2) = win32gui.GetCursorInfo()
	win32api.SetCursorPos((pos1 - x * coeff, pos2 + y * coeff))

def clickornot():
	print(keypoints['left_eye'])
	if(		isclosed(blackwhite, keypoints['left_eye']) and
		not isclosed(blackwhite, keypoints['right_eye']) or 
		not isclosed(blackwhite, keypoints['left_eye']) and
			isclosed(blackwhite, keypoints['right_eye'])):

		doubleclick()

avant = (-1, -1)

blackwhite = 0

win32api.SetCursorPos((win32api.GetSystemMetrics(0) // 2, win32api.GetSystemMetrics(1) // 2))

detector = MTCNN()

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

	image = frame
	result = detector.detect_faces(image)

	if result != []:

		blackwhite = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

		keypoints = result[0]['keypoints']

		clickornot()

		if avant != (-1,-1):
			diff = (keypoints['nose'][0] - avant[0], keypoints['nose'][1] - avant[1])

			move(*diff, 10)
		
		avant = keypoints['nose']

		cv2.circle(image,(keypoints['left_eye']), 2, (0,155,255), 2)
		cv2.circle(image,(keypoints['right_eye']), 2, (0,155,255), 2)
		cv2.circle(image,(keypoints['nose']), 2, (0,155,255), 2)
	
	cv2.imshow("preview", image)

	rval, frame = vc.read()
	
	key = cv2.waitKey(50)
	
	if key == 27: # exit on ESC
		break


cv2.destroyWindow("preview")


