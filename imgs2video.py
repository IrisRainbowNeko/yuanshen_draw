import cv2
import numpy as np
from utils import *

def fget(idx):
    return cv2.imread(f'./badapple_ys/{45+idx*3}.png')

makeVideo('./badapple_ys2.avi', 1105, fget, size=(1920,1080), fps=10)