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
    (Color.RED, [170, 70, 60], [255, 255, 255]),
    (Color.RED, [0, 70, 60], [4, 255, 255]),
    (Color.GREEN, [55, 50, 30], [90, 255, 255]),
    (Color.BLUE, [98, 100, 100], [139, 255, 255]),
    (Color.YELLOW, [24, 10, 60], [55, 255, 255]),
    (Color.ORANGE, [0, 0, 0], [255, 60, 60]),
    (Color.WHITE, [0, 0, 80], [255, 70, 255]),
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
def detect_color(img, id: int, x: int, y: int, w=4, h=4) -> Color:
    cell_hsv = cv.cvtColor(img[y : y + h, x : x + w], cv.COLOR_BGR2HSV)
    cell_color: Color = Color.ORANGE # is set when a cube color is detected
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
         

    return cell_color
