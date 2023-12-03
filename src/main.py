import time
import random
import RPi.GPIO as GPIO
import kociemba
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


# Setup cameras
g_up = FaceCaptureGroup(CubeFace.UP, [(159, 119), (120, 90), (89, 64), (194, 95), (126, 49), (224, 70), (190, 48), (144, 31)])
g_back = FaceCaptureGroup(CubeFace.BACK, [(72, 99), (100, 120), (134, 147), (75, 131), (135, 180), (76, 154), (106, 186), (132, 208)])
g_left = FaceCaptureGroup(CubeFace.LEFT, [(175, 150), (212, 127), (243, 105), (172, 186), (239, 139), (170, 217), (200, 194), (239, 161)])
g_right = FaceCaptureGroup(CubeFace.RIGHT, [(80, 59), (119, 40), (139, 23), (111, 82), (185, 42), (150, 110), (186, 86), (217, 62)])
g_front = FaceCaptureGroup(CubeFace.FRONT, [(68, 149), (69, 125), (65, 92), (100, 178), (95, 111), (132, 203), (130, 176), (128, 143)])
g_down = FaceCaptureGroup(CubeFace.DOWN, [(170, 210), (168, 181), (170, 147), (199, 185), (205, 120), (233, 155), (233, 130), (239, 96)])

upper_cam = CubeCamera(0, [g_up, g_back, g_left], True)
web.app.add_camera_feed(upper_cam.gen_bytes(), "upper")

lower_cam = CubeCamera(2, [g_down, g_front, g_right], True) 
web.app.add_camera_feed(lower_cam.gen_bytes(), "lower") 

# Setup motors
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

motor1 = stepper.Motor(STEP_1, DIR_1, EN_1)
motor2 = stepper.Motor(STEP_2, DIR_2, EN_2)
motor3 = stepper.Motor(STEP_3, DIR_3, EN_3)
motor4 = stepper.Motor(STEP_4, DIR_4, EN_4)
motor5 = stepper.Motor(STEP_5, DIR_5, EN_5)
motor6 = stepper.Motor(STEP_6, DIR_6, EN_6)

# Quick access mappings between COLORS - FACES - MOTORS
face_to_motor = {CubeFace.UP: motor6, CubeFace.DOWN: motor2, CubeFace.FRONT: motor3, CubeFace.BACK: motor4, CubeFace.LEFT: motor5, CubeFace.RIGHT: motor1}
color_to_face = {Color.WHITE: CubeFace.UP, Color.YELLOW: CubeFace.DOWN, Color.GREEN: CubeFace.FRONT, Color.BLUE: CubeFace.BACK, Color.ORANGE: CubeFace.LEFT, Color.RED: CubeFace.RIGHT}

#motors = [motor1, motor2, motor3, motor4, motor5, motor6]
#for motor in motors:
#    motor.rotate_180()
#    time.sleep(1)

def unpack_colors(colors: dict[CubeFace, [Color]]):
    """
    Takes the camera output and converts into an array of colors in the order specified by the kociemba algo.
    @param colors The output of the camera's color detection
    """
    cube_state = []
    order = [CubeFace.UP, CubeFace.RIGHT, CubeFace.FRONT, CubeFace.DOWN, CubeFace.LEFT, CubeFace.BACK]
    for face in order:
        for i in range(4):
            cube_state.append(colors[face][i])
        cube_state.append(list(color_to_face.keys())[list(color_to_face.values()).index(face)])
        for i in range(4, 8):
            cube_state.append(colors[face][i])

    return cube_state

# Used to abort solves/scrambles
abort_flag = False  

def solve() -> bool:
    time = start.now()
    cube_state = unpack_colors(upper_cam.capture_results | lower_cam.capture_results)
    cube_string = ""
    for color in cube_state:
        cube_string += color_to_face[color].value
    try:    
        moves = kociemba.solve(cube_string)
    except:
        print("Invalid cube string!")
        return False
    
    i = 0
    while i < len(moves):
        global abort_flag
        if abort_flag:
            abort_flag = False
            return False
        face = next(member for member in CubeFace.__members__.values() if member.value == moves[i])              

        if i == (len(moves) - 1) or moves[i + 1] == ' ':
            print(f"{face} clockwise")
            face_to_motor[face].rotate_cw()
            i += 2
        elif moves[i + 1] == "'":
            print(f"{face} counterclockwise")
            face_to_motor[face].rotate_ccw()
            i += 3
        elif moves[i + 1] == "2":
            print(f"{face} clockwise 180")
            face_to_motor[face].rotate_180()
            i += 3
        time.sleep(0.1)
    print(f'Solved in {start - time.now()}s')
    return True


def scramble():
    motors = [motor1, motor2, motor3, motor4, motor5, motor6]
    for _ in range(20):
        global abort_flag
        if abort_flag:
            abort_flag = False
            return
        m = random.choice(motors)
        random.choice([m.rotate_cw, m.rotate_ccw, m.rotate_180])()
        time.sleep(0.05)
    return


def abort():
    global abort_flag
    abort_flag = True
    return

# Bind functions to the web app
web.app.bind_solve_fn(solve)
web.app.bind_scramble_fn(scramble)
web.app.bind_abort_fn(abort)

# Start flask server
web.app.start()
