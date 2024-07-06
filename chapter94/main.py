import pyautogui as gui
import keyboard
from PIL import Image, ImageGrab
import time
import math


def get_pixel(image, x, y):

    px = image.load()
    return px[x, y]


def start():
    x, y, width, height = 0, 102, 1920, 872

    jump_time = 0
    last_jump_time = 0
    current_jump_time = 0
    last_interval_time = 0


    y_search1, y_search2, x_start, x_end = 557, 486, 400, 415
    y_search_for_bird = 460

    time.sleep(3)
    while True:
        t1 = time.time()
        # press q to exit the robot
        if keyboard.is_pressed("q"):
            break

        sct_img = gui.screenshot(region=(x, y, width, height))
        sct_img.save("dino.jpg")

        bg_color = get_pixel(sct_img, 100, 100)

        for i in reversed(range(x_start, x_end)):
            if (
                get_pixel(sct_img, i, y_search1) != bg_color
                or get_pixel(sct_img, i, y_search2) != bg_color
            ):
                keyboard.press("up")
                jump_time = time.time()
                current_jump_time = jump_time
                break
            if get_pixel(sct_img, i, y_search_for_bird) != bg_color:
                keyboard.press("down")
                time.sleep(0.4)
                keyboard.release("down")
                break

        interval_time = current_jump_time - last_jump_time

        if last_interval_time != 0 and math.floor(interval_time) != math.floor(last_interval_time):
            x_end += 4
            if x_end >= width:
                x_end = width

        last_jump_time = jump_time
        last_interval_time = interval_time


start()
