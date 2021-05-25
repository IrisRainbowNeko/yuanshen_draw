from draw import *
import time

from pykeyboard import PyKeyboardEvent
from threading import Thread

flag=[False] #避免多线程不共享

class Keyb(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)

    def tap(self, keycode, character, press):
        if press and keycode==83:
            print('stop')
            flag[0]=True
            exit(0)

time.sleep(2)
k = Keyb()
Thread(target=k.run).start()
for x in range(3000,3450,3):
    if flag[0]:
        break
    print(x)
    draw_img(f'badapple/{x}_badapple.flv')
    time.sleep(op.wait_time)
    window_capture(f'badapple_ys/{x}.png')
    time.sleep(op.wait_time)
    clear()