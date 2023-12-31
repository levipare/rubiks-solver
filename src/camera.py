import cv2 as cv
from enum import Enum
from threading import Thread
import time

from color import Color, detect_color, COLOR_DISPLAYS

class CubeFace(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    FRONT = "F"
    BACK = "B"

class FaceCaptureGroup:
    
    def __init__(self, face_name: CubeFace, facelets: [(int, int)]):
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


        # reset the last detected color
        for group in self.__capture_groups:
            self.capture_results[group.face_name] = [None for _ in range(len(group.facelets))]
        # Launch video capture
        self.__cap = cv.VideoCapture(index)
        if not self.__cap.isOpened():
            print(f"Cannot open camera index: {index}")
            exit()
        self.__cap.set(cv.CAP_PROP_FPS, 10)         
        self.__cap.set(cv.CAP_PROP_FRAME_WIDTH,320)
        self.__cap.set(cv.CAP_PROP_FRAME_HEIGHT,240)
        
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
                # loop through each facelet of the face 
                for i in range(len(group.facelets)):
                    x = group.facelets[i][0]
                    y = group.facelets[i][1]
                    detection = detect_color(frame, i, x, y) 
                    if detection:
                        self.capture_results[group.face_name][i] = detection
                        
                    cv.rectangle(frame, (x, y), (x + 4, y + 4), COLOR_DISPLAYS[self.capture_results[group.face_name][i]] if self.capture_results[group.face_name][i] else (0,0,0),-1)
                    cv.putText(frame, str(i), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.25, (255,255,255), 1, cv.LINE_AA, False)
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
