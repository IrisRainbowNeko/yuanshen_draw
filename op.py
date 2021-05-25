from pymouse import PyMouse
import numpy as np
import time

wait_time=0.04

mouse = PyMouse()
put_center = np.array([960,540]) #默认摆放位置
rot_offset=np.array([0,194]) #旋转条偏移

def press(pos):
    mouse.press(int(pos[0]), int(pos[1]))
    time.sleep(wait_time)

def release(pos):
    mouse.release(int(pos[0]), int(pos[1]))
    time.sleep(wait_time)

def click(pos):
    mouse.click(int(pos[0]), int(pos[1]))
    time.sleep(wait_time)

def move(pos):
    mouse.move(int(pos[0]), int(pos[1]))
    time.sleep(wait_time)


def move_to(pos):
    press(put_center)
    move(pos)
    release(pos)

def rot_to(pos, ang):
    start_pos=pos+rot_offset
    end_pos=pos+np.array([-rot_offset[1]*np.sin(ang), rot_offset[1]*np.cos(ang)])
    press(start_pos)
    move(end_pos)
    release(end_pos)