import cv2

def runWebcam():
	# From https://stackoverflow.com/questions/34588464/
	# python-how-to-capture-image-from-webcam-on-click-using-opencv
	# 1.creating a video object
	video = cv2.VideoCapture(0) 
	# 2. Variable
	a = 0
	# 3. While loop
	while True:
	    a = a + 1
	    # 4.Create a frame object
	    check, frame = video.read()
	    # Converting to grayscale
	    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	    # 5.show the frame!
	    cv2.imshow("Capturing",frame)
	    # 6.for playing 
	    key = cv2.waitKey(1)
	    if key == ord('q'):
	        break
	# 7. image saving
	showPic = cv2.imwrite("filename.jpg",frame)
	print(showPic)
	# 8. shutdown the camera
	video.release()
	cv2.destroyAllWindows 

runWebcam()

