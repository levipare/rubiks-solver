import cv2 as cv
from enum import Enum
from threading import Thread
import time

from color import Color, detect_color

class CubeFace(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    FRONT = "F"
    BACK = "B"

class FaceCaptureGroup:
    
    def __init__(self, face_name: CubeFace, facelets: [[(int, int)]]):
        """
        @param face_name The face identifier of the capture group
        @param facelets is a list containing 9 sublists that represent the 1-9 facelets of a rubik's cube face.
        Each sub list can have multiping color detection points (x,y).
        The facelet to index mapping is as follows:\n
        0 1 2\n
        3 4 5\n
        6 7 8\n
        """
        self.face_name = face_name
        self.facelets = facelets  


class CubeCamera:
    capture_results: dict[CubeFace, list[Color]] = {}

    def __init__(self, index: int, capture_groups: [FaceCaptureGroup], threaded = False):
        # Store the provided groups based off their face name
        self.__capture_groups: [FaceCaptureGroup] = capture_groups

        # Launch video capture
        self.__cap = cv.VideoCapture(index, cv.CAP_DSHOW)
        if not self.__cap.isOpened():
            print(f"Cannot open camera index: {index}")
            exit()

        # Handle the threaded capture
        if threaded:
            t = Thread(target=self.__cap_frames)
            t.start()
        else:
            self.__cap_frames()

    def __del__(self):
        # When everything done, release the capture
        self.__cap.release()

    # Private Methods

    def __cap_frames(self):
        """
        Private helper method for capturing and processing frames
        """
        while True:
            # Capture frame-by-frame
            ret, frame = self.__cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("error: no frame")
                break
            
            # loop through all faces associated with the camera
            for group in self.__capture_groups:
                # reset the last detected color
                self.capture_results[group.face_name] = []
                # loop through each facelet of the face
                for facelet in group.facelets:
                    detected_color: Color = None

                    # loop through the detection point(s) of each facelet
                    for point in facelet:
                        self.capture_results[group.face_name].append(detect_color(frame, point[0], point[1]))
                    # append the detected color 
                    self.capture_results[group.face_name].append(detected_color)
 

            self.__current_frame = frame

    
    # Public Methods

    def gen_bytes(self):
        """
        A generator that yields http encoded frames
        """
        while True:
            if not self.__current_frame.any():
                continue
            start = time.time()
            _, buffer = cv.imencode(".jpg", self.__current_frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

            time.sleep(
                max(0.033 - time.time() - start, 0)
            )  # restrict to polling every 1/30 seconds
