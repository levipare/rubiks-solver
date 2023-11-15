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
COLOR_LIMITS = {
    Color.RED: ([170, 80, 80], [255, 255, 255]),
    Color.GREEN: ([60, 50, 50], [90, 255, 255]),
    Color.BLUE: ([98, 50, 50], [139, 255, 255]),
    Color.YELLOW: ([24, 100, 100], [60, 255, 255]),
    Color.ORANGE: ([2, 150, 150], [12, 255, 255]),
    Color.WHITE: ([0, 0, 100], [255, 40, 255]),
}

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
def detect_color(img, x: int, y: int, w=5, h=5) -> Color:
    cell_hsv = cv.cvtColor(img[y : y + h, x : x + w], cv.COLOR_BGR2HSV)
    cell_color: Color = None  # is set when a cube color is detected
    most_non_zero = 0  # tracks the most dominant color in a cell

    for k, v in COLOR_LIMITS.items():
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
    img[y : y + h, x : x + w] = cv.cvtColor(cell_hsv, cv.COLOR_HSV2BGR)

    cv.rectangle(
        img,
        (x, y),
        (x + w, y + h),
        COLOR_DISPLAYS[cell_color] if cell_color else (0, 0, 0),
        -1,
    )

    return cell_color