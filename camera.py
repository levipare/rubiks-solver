import numpy as np
import cv2 as cv
from enum import Enum
from threading import Thread
import time


class Color(Enum):
    RED = "r"
    BLUE = "b"
    GREEN = "g"
    ORANGE = "o"
    YELLOW = "y"
    WHITE = "w"


# lower and upper bounds in hsv
COLOR_LIMITS = {
    Color.RED: ([170, 140, 121], [255, 255, 255]),
    Color.GREEN: ([60, 50, 50], [90, 255, 255]),
    Color.BLUE: ([98, 50, 50], [139, 255, 255]),
    Color.YELLOW: ([24, 128, 142], [40, 255, 255]),
    Color.ORANGE: ([1, 150, 150], [12, 255, 255]),
    Color.WHITE: ([0, 0, 128], [255, 25, 255]),
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
def detect_color(img, x: int, y: int, w=10, h=10):
    cell_hsv = cv.cvtColor(img[y : y + h, x : x + w], cv.COLOR_BGR2HSV)
    cell_color: Color = None  # is changed when a cube color is detected
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


class CubeCamera:
    def __init__(self, index: int):
        self.index = index

        # launch video capture
        self.cap = cv.VideoCapture(index)
        if not self.cap.isOpened():
            print(f"Cannot open camera index: {index}")
            exit()

    def __del__(self):
        # When everything done, release the capture
        self.cap.release()

    def __cap_frames(self):
        """
        Private helper method for captureing and processing frames
        """
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("no frame")
                break

            frame = cv.flip(frame, 1)

            size = 400  # size of box on screen
            h, w, _ = frame.shape
            origin = (int((w - size) / 2), int((h - size) / 2))

            # Create slices of the frame for each cell
            for row in range(3):
                for col in range(3):
                    offsetX = int(size / 3) * col
                    offsetY = int(size / 3) * row
                    startX = origin[0] + offsetX
                    startY = origin[1] + offsetY

                    detect_color(frame, startX, startY)

            # cv.imshow("frame", self.frame)

            self.current_frame = frame

    def capture_frames(self, threaded: bool = False):
        """
        Starts the processing of frames with the option of it being non-blocking
        """
        if threaded:
            t = Thread(target=self.__cap_frames)
            t.start()
        else:
            self.__cap_frames()

    def gen_bytes(self):
        """
        A generator that yields http encoded frames
        """
        while True:
            if not self.current_frame.any():
                continue
            start = time.time()
            _, buffer = cv.imencode(".jpg", self.current_frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

            time.sleep(
                max(0.033 - time.time() - start, 0)
            )  # restrict to polling every 1/30 seconds
