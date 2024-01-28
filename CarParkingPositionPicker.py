
#CarParkingPositionPicker.py
# Importing packages
import cv2
import pickle

# setting width & height of the space for a single car
width, height = 106, 47

# Loading from earlier positions that were set previously
try:
    with open('CarParkingPositions', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# funtion to do the operation based on left click or right click
def clickMouse(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        # draw & add the rectangle parking position
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                # remove rectangle parking position at the clicked place
                posList.pop(i)
                print(i)

    with open('CarParkingPositions', 'wb') as f:
        pickle.dump(posList, f)


while True:
    # loading the image from the car parking image frame
    img = cv2.imread('carParkingFrameImg.png')

    # looping the drawn positions previously and draw the rectangle
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 255, 0), 3)

    # display the image to view the marked positions
    cv2.imshow("Image", img)

    # callback method for the mouse click event
    cv2.setMouseCallback("Image", clickMouse)

    # based on this millsec time , speed of the video will be regulated.
    cv2.waitKey(1)