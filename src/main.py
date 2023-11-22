import time
import RPi.GPIO as GPIO
import kociemba
import cv2
import stepper
from camera import CubeCamera, CubeFace, FaceCaptureGroup
from color import Color
import web.app

# MOTOR PIN MAPPINGS
# DO NOT CHANGE
STEP_1 = 37
STEP_2 = 33
STEP_3 = 15
STEP_4 = 38
STEP_5 = 32
STEP_6 = 16

DIR_1 = 35
DIR_2 = 31
DIR_3 = 13
DIR_4 = 40
DIR_5 = 36
DIR_6 = 18

EN_1 = 29
EN_2 = 21
EN_3 = 19
EN_4 = 26
EN_5 = 24
EN_6 = 10

g_up = FaceCaptureGroup(CubeFace.UP, [(92,67), (133, 42), (152, 25), (125, 89), (201, 45), (164, 112), (201, 92), (235, 69)])
g_back = FaceCaptureGroup(CubeFace.BACK, [(75, 92), (108, 117), (141, 143), (80, 126), (141, 180), (80, 151), (115, 187), (142, 208)])
g_left = FaceCaptureGroup(CubeFace.LEFT, [(178, 149), (216, 124), (248, 103), (175, 185), (242, 135), (172, 214), (203, 191), (245, 158)])
g_right = FaceCaptureGroup(CubeFace.RIGHT, [(92, 59), (126, 40), (179, 25), (120, 86), (197, 45), (155, 113), (196, 90), (232, 68)])
g_front = FaceCaptureGroup(CubeFace.FRONT, [(73, 149), (75, 126), (71, 92), (107, 185), (102, 119), (131, 208), (135, 182), (133, 146)])
g_down = FaceCaptureGroup(CubeFace.DOWN, [(167, 213), (168, 186), (169, 154), (196, 191), (208, 126), (236, 158), (236, 138), (242, 105)])

upper_cam = CubeCamera(0, [g_up, g_back, g_left], True) # start upper camera capture
web.app.add_camera_feed(upper_cam.gen_bytes(), "upper") # send cam feed to flask app

lower_cam = CubeCamera(2, [g_right, g_front, g_down], True) 
web.app.add_camera_feed(lower_cam.gen_bytes(), "lower") 


GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

motor1 = stepper.Motor(STEP_1, DIR_1, EN_1)
motor2 = stepper.Motor(STEP_2, DIR_2, EN_2)
motor3 = stepper.Motor(STEP_3, DIR_3, EN_3)
motor4 = stepper.Motor(STEP_4, DIR_4, EN_4)
motor5 = stepper.Motor(STEP_5, DIR_5, EN_5)
motor6 = stepper.Motor(STEP_6, DIR_6, EN_6)


motors = [motor1, motor2, motor3, motor4, motor5, motor6]
#import random
#for _ in range(20):
#    m = random.choice(motors)
#    m.rotate_cw()
#    time.sleep(0.2)


color_to_face = {Color.WHITE: CubeFace.UP, Color.YELLOW: CubeFace.DOWN, Color.GREEN: CubeFace.FRONT, Color.BLUE: CubeFace.BACK, Color.GREEN: CubeFace.LEFT, Color.RED: CubeFace.RIGHT}

def unpack_colors(colors: dict[CubeFace, [Color]]):
    color_string = ""
    order = [CubeFace.UP, CubeFace.RIGHT, CubeFace.FRONT, CubeFace.DOWN, CubeFace.LEFT, CubeFace.BACK]
    for face in order:
        for i in range(9):
                if i == 5:
                    color_string += face.value
                else:
                    color_string += colors[face][i].value if colors[face][i] else " "
    return color_string
    


def solve():
    print("SOLVING")
    color_string = unpack_colors(upper_cam.capture_results | lower_cam.capture_results)
    print(color_string)
 
    # FORMAT: URFDLB
    return

# Bind solve to the web app's /solve route
web.app.bind_solve_fn(solve)

# Start flask server
web.app.start()
