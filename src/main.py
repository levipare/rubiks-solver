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
g_back = FaceCaptureGroup(CubeFace.BACK, [(72, 99), (100, 120), (134, 147), (75, 131), (135, 180), (76, 157), (106, 186), (132, 208)])
g_left = FaceCaptureGroup(CubeFace.LEFT, [(175, 150), (212, 127), (243, 105), (172, 186), (239, 139), (170, 217), (200, 194), (239, 161)])
g_right = FaceCaptureGroup(CubeFace.RIGHT, [(80, 59), (119, 40), (173, 20), (111, 82), (185, 42), (150, 110), (186, 86), (217, 62)])
g_front = FaceCaptureGroup(CubeFace.FRONT, [(72, 146), (69, 125), (65, 92), (100, 178), (95, 111), (132, 203), (130, 176), (128, 143)])
g_down = FaceCaptureGroup(CubeFace.DOWN, [(170, 210), (168, 181), (170, 147), (199, 185), (205, 120), (233, 155), (233, 130), (239, 96)])

g_one = FaceCaptureGroup(CubeFace.FRONT, [(71, 92), (97, 111), (131, 143)])

upper_cam = CubeCamera(0, [], True)
web.app.add_camera_feed(upper_cam.gen_bytes(), "upper")

lower_cam = CubeCamera(2, [g_one], True) 
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

def unpack_colors(colors: dict[CubeFace, [Color]]) -> [Color]:
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

def color_lit_to_enum(colors: str) -> [Color]:
    ce = []
    for c in colors:
        ce.append(Color(c))
    return ce     

def get_state_str():
    cube_state = unpack_colors(upper_cam.capture_results | lower_cam.capture_results)
    s = ""
    for c in cube_state:
        s += c.value if c else ' '
    return s

def turn_to_get_state() -> [Color]:
    delay = 1
    UP = face_to_motor[CubeFace.UP]
    DOWN = face_to_motor[CubeFace.DOWN]
    LEFT = face_to_motor[CubeFace.LEFT]
    RIGHT = face_to_motor[CubeFace.RIGHT]
    FRONT = face_to_motor[CubeFace.FRONT]
    BACK = face_to_motor[CubeFace.BACK]

    # Up scanning
    up_state = [None for _ in range(9)]
    up_state[4] = Color.WHITE
    RIGHT.rotate_ccw()
    time.sleep(delay)
    (up_state[2], up_state[5], up_state[8]) = lower_cam.capture_results[CubeFace.FRONT]
    RIGHT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_ccw()
    time.sleep(delay)
    up_state[0] = lower_cam.capture_results[CubeFace.FRONT][0]
    up_state[1] = lower_cam.capture_results[CubeFace.FRONT][1]
    RIGHT.rotate_cw()
    time.sleep(0.05) 
    UP.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_ccw()
    time.sleep(delay)    
    up_state[3] = lower_cam.capture_results[CubeFace.FRONT][1]
    up_state[6] = lower_cam.capture_results[CubeFace.FRONT][0]
    RIGHT.rotate_cw()
    time.sleep(0.05) 
    UP.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_ccw()
    time.sleep(delay)
    up_state[7] = lower_cam.capture_results[CubeFace.FRONT][1]
    RIGHT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_cw()

    # Right scanning
    right_state = [None for _ in range(9)]
    right_state[4] = Color.RED
    time.sleep(delay)    
    UP.rotate_cw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay)
    
    (right_state[0], right_state[1], right_state[2]) = lower_cam.capture_results[CubeFace.FRONT]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_ccw()   
    time.sleep(0.05)
    RIGHT.rotate_cw()
    
    UP.rotate_cw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay)
 
    right_state[6] = lower_cam.capture_results[CubeFace.FRONT][0]
    right_state[3] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_ccw()   
    time.sleep(0.05)
    RIGHT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay)
    right_state[8] = lower_cam.capture_results[CubeFace.FRONT][0]
    right_state[7] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_ccw()   
    time.sleep(0.05)
    RIGHT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay)
    right_state[5] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_ccw()   
    time.sleep(0.05)
    RIGHT.rotate_cw()

   
    # Front scanning
    front_state = [None for _ in range(9)]
    front_state[4] = Color.GREEN
    
    time.sleep(delay)    
    (front_state[2], front_state[5], front_state[8]) = lower_cam.capture_results[CubeFace.FRONT]
    FRONT.rotate_cw()
    time.sleep(delay)
    front_state[0] = lower_cam.capture_results[CubeFace.FRONT][0] 
    front_state[1] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_cw()
    time.sleep(delay)
    front_state[6] = lower_cam.capture_results[CubeFace.FRONT][0] 
    front_state[3] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_cw()
    time.sleep(delay)
    front_state[7] = lower_cam.capture_results[CubeFace.FRONT][1] 
    FRONT.rotate_cw()

    # Down scanning
    down_state = [None for _ in range(9)]
    down_state[4] = Color.YELLOW
    time.sleep(delay) 
    RIGHT.rotate_cw()
    time.sleep(delay) 
    (down_state[2], down_state[5], down_state[8]) = lower_cam.capture_results[CubeFace.FRONT]
    RIGHT.rotate_ccw()
    time.sleep(0.05)
    DOWN.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_cw()
    time.sleep(delay)         
    down_state[0] = lower_cam.capture_results[CubeFace.FRONT][0] 
    down_state[1] = lower_cam.capture_results[CubeFace.FRONT][1]
    RIGHT.rotate_ccw()
    time.sleep(0.05) 
    DOWN.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_cw()
    time.sleep(delay)
    down_state[6] = lower_cam.capture_results[CubeFace.FRONT][0] 
    down_state[3] = lower_cam.capture_results[CubeFace.FRONT][1]
    RIGHT.rotate_ccw()
    time.sleep(0.05) 
    DOWN.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_cw()
    time.sleep(delay)
    down_state[7] = lower_cam.capture_results[CubeFace.FRONT][1] 

    RIGHT.rotate_ccw()
    time.sleep(0.05) 
    DOWN.rotate_cw()
    time.sleep(0.05)

    # Left scanning    
    left_state = [None for _ in range(9)]
    left_state[4] = Color.ORANGE
    time.sleep(delay)
    UP.rotate_ccw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay) 
    (left_state[0], left_state[1], left_state[2]) = lower_cam.capture_results[CubeFace.FRONT]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    LEFT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_ccw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay) 
    left_state[6] = lower_cam.capture_results[CubeFace.FRONT][0] 
    left_state[3] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    LEFT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_ccw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay) 
    left_state[8] = lower_cam.capture_results[CubeFace.FRONT][0] 
    left_state[7] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    LEFT.rotate_cw()
    time.sleep(0.05)
    UP.rotate_ccw()
    time.sleep(0.05)
    FRONT.rotate_cw()
    time.sleep(delay) 
    left_state[5] = lower_cam.capture_results[CubeFace.FRONT][1]
    FRONT.rotate_ccw()
    time.sleep(0.05)
    UP.rotate_cw()
    time.sleep(0.05)
    LEFT.rotate_cw()

    # Back scanning    
    back_state = [None for _ in range(9)]
    back_state[4] = Color.BLUE
    time.sleep(delay)
    RIGHT.rotate_180()
    time.sleep(delay) 
    (back_state[6], back_state[3], back_state[0]) = lower_cam.capture_results[CubeFace.FRONT]
    RIGHT.rotate_180()
    time.sleep(0.05)
    BACK.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_180()
    time.sleep(delay)
    back_state[8] = lower_cam.capture_results[CubeFace.FRONT][0] 
    back_state[7] = lower_cam.capture_results[CubeFace.FRONT][1]
    RIGHT.rotate_180()
    time.sleep(0.05)
    BACK.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_180()
    time.sleep(delay)
    back_state[2] = lower_cam.capture_results[CubeFace.FRONT][0] 
    back_state[5] = lower_cam.capture_results[CubeFace.FRONT][1]
    RIGHT.rotate_180()
    time.sleep(0.05)
    BACK.rotate_cw()
    time.sleep(0.05)
    RIGHT.rotate_180()
    time.sleep(delay)
    back_state[1] = lower_cam.capture_results[CubeFace.FRONT][1] 

    RIGHT.rotate_180()
    time.sleep(0.05)
    BACK.rotate_cw()
    time.sleep(0.05)


    return up_state + right_state + front_state + down_state + left_state + back_state


# Used to abort solves/scrambles
abort_flag = False  

def solve(color_string: str = None) -> bool:
    cube_string = ""
    if color_string:
        for color in color_lit_to_enum(color_string):
            cube_string += color_to_face[color].value
    else:
        state = turn_to_get_state()
        print(state)
        for color in state:
            cube_string += color_to_face[color].value
    
    try:    
        moves = kociemba.solve(cube_string)
    except:
        print(f"Invalid cube string! {cube_string}")
        return False

    for i in range(7):
        print(f"About to solve in {7-i}s")
        time.sleep(1)
    start = time.time()
    
    # dummy solve to contribute to time
    kociemba.solve(cube_string)
    i = 0
    while i < len(moves):
        global abort_flag
        if abort_flag:
            abort_flag = False
            return False
        face = CubeFace(moves[i])              

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
        time.sleep(0.01)
    print(f'Solved in {time.time() - start:.2f}s')
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
        time.sleep(0.01)
    return


def abort():
    global abort_flag
    abort_flag = True
    return

# Bind functions to the web app
web.app.bind_solve_fn(solve)
web.app.bind_scramble_fn(scramble)
web.app.bind_abort_fn(abort)
web.app.bind_state_fn(get_state_str)

# Start flask server
web.app.start()
