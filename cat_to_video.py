import pickle
import numpy as np
from utils import *

#将储存的线段可视化为视频
def fget(idx):
    with open(f"./badapple/{45+idx*3}_badapple.flv.pkl", "rb") as f:
        line_list = pickle.load(f)

        cts = np.zeros((500, 668, 3), dtype=np.uint8)
        cv2.polylines(cts, [x[:, np.newaxis, :] for x in line_list], False, (255, 255, 255), 1)
        return cts

makeVideo('./badapple_line.avi', 1105, fget, size=(668,500), fps=10)