# import twophase.solver as sv
# import twophase.cubie as cubie
import time
import RPi.GPIO as GPIO
from camera import CubeCamera
import web.app
import stepper


# Instantiate first camera and its corresponding web feed
#camera0 = CubeCamera(0)
#camera0.capture_frames(threaded=True)
#web.app.create_camera_feed(camera0.gen_bytes())

GPIO.setmode(GPIO.BOARD)

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

motor1 = stepper.Motor(STEP_1, DIR_1)
motor2 = stepper.Motor(STEP_2, DIR_2)
motor3 = stepper.Motor(STEP_3, DIR_3)
motor4 = stepper.Motor(STEP_4, DIR_4)
motor5 = stepper.Motor(STEP_5, DIR_5)
motor6 = stepper.Motor(STEP_6, DIR_6)


motor3.rotate_180()


GPIO.cleanup()

exit(0)

def solve():
    # cc = cubie.CubieCube()
    # cc.randomize()
    # fc = cc.to_facelet_cube()
    # cubestring = fc.to_string()
    # cubestring = "ULRRUBUBFDRFURBRFLRDLFFRLLDBUBUDDUDBBDFRLULBUDFRLBFDLF"
    # print(sv.solve(cubestring, 20, 1))
    print("solving")

# Bind solve to the web app's /solve route
web.app.bind_solve_fn(solve)

# Start flask server
web.app.start()
