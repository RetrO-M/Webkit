from sys import stdout
from rgbprint import Color
import datetime


white = Color.ghost_white
blue = Color.sky_blue
magenta = Color.magenta

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write(f"\r{magenta}[+]{white} Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + f"{blue} sec left")
            return