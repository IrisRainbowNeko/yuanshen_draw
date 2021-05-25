import cv2
import numpy as np
import pickle
from utils import *

def get_lines(img, name, show=True, scale_factor=1.0):
    #将图像转化为灰度图像
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #获取边缘图
    edge = get_edge(imgray)
    if show:
        cv2.imshow("edge", edge)

    #获取边缘矢量
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)

    #过滤掉长度过短的
    contours=[x*scale_factor for x in contours if len(x)>10]
    print(len(contours))

    line_list=to_lines(contours, dist_thr=[55, 45]) #将轮廓转换为定长的线段
    line_list=list2lines(line_list)
    line_list=rm_close_lines2(line_list, dist_thr=(20,20)) #过滤相交和重叠线段
    #line_list=rm_close_lines(line_list, dist_thr=40)
    line_list=lines2list(line_list)

    #储存线段
    with open(rf"./{name}.pkl", "wb") as f:
        pickle.dump(line_list, f)

    print(len(line_list), edge.dtype)
    if show:
        cts=np.zeros(list(edge.shape)+[3], dtype=edge.dtype)
        cv2.polylines(cts, [x[:,np.newaxis,:] for x in line_list], False, (255, 255, 255), 1)
        cv2.imshow("fuck",cts)
        cv2.waitKey()


#图像转为线段
#img_name='bap.png'
#img = cv2.imread(f'./{img_name}')
#img = cv2.resize(img, (667,500), interpolation = cv2.INTER_AREA)

#视频按帧转为线段
vid_path='badapple.flv'
video = cv2.VideoCapture(f'./{vid_path}')
count=0
while (True):
    ret, frame = video.read()
    if ret is False:
        video.release()
        break

    frame = cv2.resize(frame, (667, 500), interpolation=cv2.INTER_AREA)
    get_lines(frame, f'badapple/{count}_{vid_path}', show=False, scale_factor=0.9)
    count += 1
    #break