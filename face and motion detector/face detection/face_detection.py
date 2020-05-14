# import cv2
# img = cv2.imread("face.jpg",1)

# # resize the image to smaller image
# resized = cv2.resize(img, (int(img.shape[1]/2),int(img.shape[0]/2)))
# cv2.imshow("legend", resized)
# # window will stay open for 2000 mil/sec
# cv2.waitKey(2000)

# cv2.destroyAllWindows()

import cv2

# create a cascadeclassifier
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# read our image
img = cv2.imread("face.jpg")
# read the image as a gray scale 
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# search for the cordinates of the image, set scale factor = 1.05 and minnighbors = 5
faces = face_cascade.detectMultiScale(gray_img,  1.05, 5)

print(type(faces))
print(faces)

color = (0,255,0)
# for loop to display a box around the face

for x,y,w,h in faces:
    img = cv2.rectangle(img, (x,y), (x+w, y+h), color , 3 )
cv2.imshow("gray", img)
cv2.waitKey(0)
cv2.destroyAllWindows()