import kociemba
from camera import CubeFace
from color import Color

color_to_face = {Color.WHITE: CubeFace.UP, Color.YELLOW: CubeFace.DOWN, Color.GREEN: CubeFace.FRONT, Color.BLUE: CubeFace.BACK, Color.ORANGE: CubeFace.LEFT, Color.RED: CubeFace.RIGHT}


def solve():
    cube_string = ""
    for color in cube_state:
        cube_string += color_to_face[color]
    cube_string = 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'
    moves = kociemba.solve(cube_string)
    i = 0
    while i < len(moves):
        face = moves[i]
        if i == (len(moves) - 1) and moves[i + 1] == ' ':
            print(f"{face} clockwise")
            i += 2
        elif moves[i + 1] == "'":
            print(f"{face} counterclockwise")
            i += 3
        elif moves[i + 1] == "2":
            print(f"{face} clockwise 180")
            i += 3
        




    


