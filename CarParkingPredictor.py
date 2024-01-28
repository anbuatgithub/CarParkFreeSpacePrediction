# Importing packages
import cv2
import pickle
import cvzone
import numpy as np

# Video feed from the Clip. Ideally has to be imported from Connected Camera
cap = cv2.VideoCapture('carParkingVideo.mp4')

# Loading from earlier positions that were set using CarParkingPositionPicker program
with open('CarParkingPositions', 'rb') as f:
    posList = pickle.load(f)

# setting width & height of the space for a single car
width, height = 106, 47


# Funtion to detect free space & change the display
def check_free_space(imgPro):
    space_counter = 0

    for pos in posList:
        x, y = pos
        # cropping the individual car space images
        img_crop = imgPro[y:y + height, x:x + width]

        #cv2.imshow(str(x * y), img_crop)

        # Counting the pixel size from the dilated image
        count = cv2.countNonZero(img_crop)

        # if the count value is less than threshold value , the assumed as free space
        if count < 900:
            color = (0, 255,0)
            thickness = 3
            space_counter += 1
        # else occupied
        else:
            color = (120, 51, 155)
            thickness = 3

        # drawing the rectangle for all the captures car park positions
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # Printing the pixel count value inside each car parking position
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=1, offset=0, colorR=color)
        # displaying the spaces
        cvzone.putTextRect(img, f'Total Spaces: {len(posList)} | Occupied Spaces: {len(posList)-space_counter}'
                                f' | Free Spaces: {space_counter} ', (50, 50), scale=2, thickness=2, offset=5, colorR=(2000, 0, 0))
        # Static text
        cvzone.putTextRect(img, f'ECS7016W - Car Parking Free Space Prediction : ANBALAGAN M', (5, 703), scale=2,
                           thickness=2, offset=5, colorR=(2000, 0, 0))


while True:
    # condition to check the total frame size & make it continue to play the vido clip again when finished.
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # capturing the image from video
    success, img = cap.read()
    # converting into gray scale image
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # make it as blurred
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # getting threshold image to see the edges and corners
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # removing extra edge & corners scales
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # calling the fuction to detect free space
    check_free_space(imgDilate)
    # to show the actual application
    cv2.imshow("CarParkFreeSpacePredictor", img)
    #cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("imgDilate", imgDilate)
    cv2.waitKey(10)
