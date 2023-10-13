# import twophase.solver as sv
# import twophase.cubie as cubie
import RPi.GPIO as GPIO
from camera import CubeCamera
import web.app
import stepper


# Instantiate first camera and its corresponding web feed
#camera0 = CubeCamera(0)
#camera0.capture_frames(threaded=True)
#web.app.create_camera_feed(camera0.gen_bytes())

GPIO.setmode(GPIO.BOARD)

# Instantiate motors
STEP_1 = 37
STEP_2 = 33
STEP_3 = 15

DIR_1 = 35
DIR_2 = 31
DIR_3 = 13

motor0 = stepper.Motor(STEP_1, DIR_1, 500)
motor1 = stepper.Motor(STEP_2, DIR_2, 500)
motor2 = stepper.Motor(STEP_3, DIR_3, 500)


motor0.rotate_cw()
motor1.rotate_cw()
motor2.rotate_cw()


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
