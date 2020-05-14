
import cv2, time

#use cv2 function to capture image using our webcam, which is set to 0
video = cv2.VideoCapture(0)

# for loop to capture multiple images which creates a vidoe
a =1 
while True:
    a=a + 1
    check, frame = video.read()
    print(frame)

    #convert into a gray scale image
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # displays the image/vidoe being captured
    cv2.imshow("captureing", gray)

    # generates a new frame every 1 mili second
    key =cv2.waitKey(1)
    #press q to close
    if key == ord("q"):
        break

print(a)

# ends our video
video.release()

cv2.destroyAllWindows()

