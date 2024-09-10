from sys import stdout
from rgbprint import Color

white = Color.ghost_white
blue = Color.sky_blue
magenta = Color.magenta

def attack_done():
    stdout.write(f"\n{magenta}[+]{white} Attack Done !\n")