# import twophase.solver as sv
# import twophase.cubie as cubie
from camera import CubeCamera
import web.app


# Instantiate first camera and its corresponding web feed
camera0 = CubeCamera(0)
camera0.capture_frames(threaded=True)
web.app.create_camera_feed(camera0.gen_bytes())


def solve():
    # cc = cubie.CubieCube()
    # cc.randomize()
    # fc = cc.to_facelet_cube()
    # cubestring = fc.to_string()
    # cubestring = "ULRRUBUBFDRFURBRFLRDLFFRLLDBUBUDDUDBBDFRLULBUDFRLBFDLF"
    # print(sv.solve(cubestring, 20, 1))
    print("here")


# Bind solve to the web app's /solve route
web.app.bind_solve_fn(solve)

# Start flask server
web.app.start()
