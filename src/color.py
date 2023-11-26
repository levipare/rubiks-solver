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
COLOR_LIMITS = [
    (Color.RED, [170, 80, 60], [255, 255, 255]),
    (Color.RED, [0, 30, 40], [3, 255, 255]),
    (Color.GREEN, [55, 50, 30], [90, 255, 255]),
    (Color.BLUE, [98, 140, 50], [139, 255, 255]),
    (Color.YELLOW, [24, 80, 60], [55, 255, 255]),
    (Color.ORANGE, [4, 90, 80], [17, 255, 255]),
    (Color.WHITE, [0, 0, 30], [255, 100, 255]),
]

# bgr
COLOR_DISPLAYS = {
    Color.RED: (0, 0, 255),
    Color.GREEN: (0, 255, 0),
    Color.BLUE: (255, 0, 0),
    Color.YELLOW: (0, 255, 255),
    Color.ORANGE: (0, 128, 255),
    Color.WHITE: (255, 255, 255),
}


# https://learnopencv.com/color-spaces-in-opencv-cpp-python/
def detect_color(img, id: int, x: int, y: int, w=5, h=5) -> Color:
    cell_hsv = cv.cvtColor(img[y : y + h, x : x + w], cv.COLOR_BGR2HSV)
    cell_color: Color = None  # is set when a cube color is detected
    most_non_zero = 0  # tracks the most dominant color in a cell

    for color in COLOR_LIMITS:
        lower = np.array(color[1])
        upper = np.array(color[2])
        mask = cv.inRange(cell_hsv, lower, upper)
        masked = cv.bitwise_and(cell_hsv, cell_hsv, mask=mask)
        flattened = masked.flatten()
        non_zero = np.count_nonzero(flattened)

        if non_zero > most_non_zero and non_zero > flattened.size * 0.2:
            most_non_zero = non_zero
            cell_color = color[0]
            cell_hsv = masked

    # Draw the masked image to its cell
    img[y : y + h, x : x + w] = cv.cvtColor(cell_hsv, cv.COLOR_HSV2BGR)

    cv.rectangle(
        img,
        (x, y),
        (x + w, y + h),
        COLOR_DISPLAYS[cell_color] if cell_color else (0, 0, 0),
        -1,
    )
    cv.putText(img, str(id), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.25, (255,255,255), 1, cv.LINE_AA, False)
    return cell_color
