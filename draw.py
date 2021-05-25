import pickle
import numpy as np
from utils import *
import op
import time

item_pos=np.array([500,970]) #围栏坐标
scale_rate=1000/500 #缩放比例
offset=np.array([960-500,540-500]) #摆放起始坐标
ok=np.array([1841,578]) #确定坐标

setting=np.array([77,48]) #设置坐标
collect_all=np.array([297,772]) #收纳所有摆设
collect_ok=np.array([1180,760])

#在原神里绘制一张线段图
def draw_img(img_name):
    with open(rf"./{img_name}.pkl", "rb") as f:
        line_list = pickle.load(f)

    line_list=list2lines(line_list)

    for line in line_list:
        l_c=line.center()*scale_rate+offset
        l_ang=line.angle()

        op.click(item_pos)
        time.sleep(op.wait_time)
        op.move_to(l_c)
        time.sleep(op.wait_time)
        op.rot_to(l_c, l_ang)
        time.sleep(op.wait_time)
        op.click(ok)
        time.sleep(op.wait_time)

#清空当前摆设
def clear():
    op.click(setting)
    time.sleep(0.2)
    op.click(collect_all)
    time.sleep(0.2)
    op.click(collect_ok)
    time.sleep(0.2)
    op.click(setting)
    time.sleep(0.2)

if __name__ == '__main__':
    time.sleep(2)
    draw_img('pm.png')