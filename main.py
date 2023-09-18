import numpy as np
import cv2 as cv
from enum import Enum


class Color(Enum):
    RED = "r"
    BLUE = "b"
    GREEN = "g"
    ORANGE = "o"
    YELLOW = "y"
    WHITE = "w"


# lower and upper bounds in hsv
color_limits = {
    Color.RED: ([170, 140, 121], [255, 255, 255]),
    Color.GREEN: ([60, 50, 50], [90, 255, 255]),
    Color.BLUE: ([98, 50, 50], [139, 255, 255]),
    Color.YELLOW: ([24, 128, 142], [40, 255, 255]),
    Color.ORANGE: ([2, 150, 201], [12, 255, 255]),
    Color.WHITE: ([0, 0, 128], [255, 25, 255]),
}


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def draw_cube_border(frame, origin, size):
    cv.rectangle(
        frame,
        (origin[0], origin[1]),
        (origin[0] + size, origin[1] + size),
        (256, 256, 256),
        2,
    )
    for i in range(2):
        offset = int(size / 3) * (i + 1)
        cv.line(
            frame,
            (origin[0] + offset, origin[1]),
            (origin[0] + offset, origin[1] + size),
            (256, 256, 256),
            2,
        )
        cv.line(
            frame,
            (origin[0], origin[1] + offset),
            (origin[0] + size, origin[1] + offset),
            (256, 256, 256),
            2,
        )


# https://learnopencv.com/color-spaces-in-opencv-cpp-python/
def capture_cells(frame, origin, size):
    # Create slices of the frame for each cell
    for row in range(3):
        for col in range(3):
            offsetX = int(size / 3) * col
            offsetY = int(size / 3) * row
            startX = origin[0] + offsetX
            startY = origin[1] + offsetY
            endX = startX + int(size / 3)
            endY = startY + int(size / 3)

            # find an corresponding cube color
            cell_hsv = cv.cvtColor(frame[startY:endY, startX:endX], cv.COLOR_BGR2HSV)
            cell_color: Color = None  # is changed when a cube color is detected
            most_non_zero = 0  # tracks the most dominant color in a cell

            for k, v in color_limits.items():
                lower = np.array(v[0])
                upper = np.array(v[1])
                mask = cv.inRange(cell_hsv, lower, upper)
                masked = cv.bitwise_and(cell_hsv, cell_hsv, mask=mask)
                flattened = masked.flatten()
                non_zero = np.count_nonzero(flattened)

                if non_zero > most_non_zero and non_zero > flattened.size * 0.2:
                    most_non_zero = non_zero
                    cell_color = k
                    cell_hsv = masked

            # Draw the masked image to its cell
            frame[startY:endY, startX:endX] = cv.cvtColor(cell_hsv, cv.COLOR_HSV2BGR)

            cv.putText(
                frame,
                cell_color.value if cell_color else None,
                (startX + 50, startY + 75),
                cv.FONT_HERSHEY_DUPLEX,
                1.5,
                (256, 256, 256),
                2,
            )


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("no frame")
        break

    frame = cv.flip(frame, 1)

    size = 400  # size of box on screen
    h, w, _ = frame.shape
    origin = (int((w - size) / 2), int((h - size) / 2))

    capture_cells(frame, origin, size)
    draw_cube_border(frame, origin, size)

    cv.imshow("frame", frame)

    # Break loop when q is pressed
    key = cv.waitKey(1)
    if key == ord("q"):
        break


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
