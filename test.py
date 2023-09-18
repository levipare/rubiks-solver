import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

test = ([0, 0, 128], [255, 25, 255])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("no frame")
        break

    frame = cv.flip(frame, 1)

    # Handle dominant color of each cell
    cell_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    char = None
    most_non_zero = 0

    lower = np.array(test[0])
    upper = np.array(test[1])
    mask = cv.inRange(cell_hsv, lower, upper)
    masked = cv.bitwise_and(cell_hsv, cell_hsv, mask=mask)
    flattened = masked.flatten()

    frame = cv.cvtColor(masked, cv.COLOR_HSV2BGR)

    cv.imshow("frame", frame)
    # Break loop when q is pressed
    key = cv.waitKey(1)
    if key == ord("q"):
        break
    if key == ord("h"):
        test[0][0] += 1
    if key == ord("s"):
        test[0][1] += 1
    if key == ord("v"):
        test[0][2] += 1
    print(test)

cap.release()
cv.destroyAllWindows()
