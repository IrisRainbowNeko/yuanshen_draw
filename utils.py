import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

class Line:

    def __init__(self, p1, p2):
        self.p1=p1
        self.p2=p2

    def center(self):
        return (self.p1+self.p2)/2

    def line_len(self):
        return max(1,np.linalg.norm(self.p1-self.p2, 2))

    def angle(self):
        llen=self.line_len()
        rad=np.arccos((self.p1[0]-self.p2[0])/llen)*np.sign(self.p1[1]-self.p2[1])
        return rad

    def dist_to(self, line):
        return np.linalg.norm(self.center()-line.center(), 2)

    def minr_rest_dist_to(self, line, pdist=lambda p1, p2:np.linalg.norm(p1-p2,2)):
        dists=(pdist(self.p1, line.p1), pdist(self.p1, line.p2), pdist(self.p2, line.p1), pdist(self.p2, line.p2))
        min_idx=np.argmin(dists)
        return dists[min_idx], dists[len(dists)-1-min_idx]

    def angel_to(self, line):
        dis_ang=np.abs(self.angle()-line.angle())
        return dis_ang if dis_ang<=np.pi/2 else (np.pi*2-dis_ang)%(np.pi/2)

    # Return true if line segments AB and CD intersect
    def intersect_to(self, line, size=4):
        #A,B,C,D = self.p1, self.p2, line.p1, line.p2
        #return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        rect1 = (self.center(), (self.line_len()+2, size*2), np.rad2deg(self.angle()))
        rect2 = (line.center(), (line.line_len()+2, size*2), np.rad2deg(line.angle()))
        r1 = cv2.rotatedRectangleIntersection(rect1, rect2)[0]
        return r1!=0

    def extend(self, exlen):
        exlen=exlen+self.line_len()
        return Line(self.center()-to_item_vec(self.p1-self.p2)*exlen/2, self.center()+to_item_vec(self.p1-self.p2)*exlen/2)


def open_demo(image,size=(5,5)):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
    binary = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return binary

def close_demo(image,size=(5,5)):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, size)
    binary = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel,anchor=(-1, -1), iterations=3)
    return binary

def get_edge(imgray):
    canny = 255 - imgray
    canny = cv2.GaussianBlur(canny, ksize=(21, 21), sigmaX=0, sigmaY=0)
    canny = 255 - cv2.divide(imgray, 255 - canny, scale=256)
    canny = cv2.Canny(canny, 40, 200)
    #canny = close_demo(canny, (3, 3))
    return canny

def to_item_vec(vec):
    return vec/np.linalg.norm(vec, 2)

def to_lines(contours, dist_thr=(42, 40), pdist=lambda p1, p2:np.linalg.norm(p1-p2,2), rm_rest=20):
    line_list=[]
    for cnt in contours:
        cnt = np.squeeze(cnt, 1)
        base = cnt[0]
        max_pos = 0
        max_dist = 1
        for idx, pos in enumerate(cnt[1:, :]):
            dist = pdist(base, pos)
            if dist > max_dist:
                max_pos = pos
                max_dist = dist

                if dist > dist_thr[0]:  # 可连成一个线段
                    center=(base+pos)/2
                    drct=to_item_vec(pos-base)*(dist_thr[1]/2)

                    line_list.append(np.array([center-drct, center+drct], np.int32).reshape((-1, 2)))
                    #line_list.append(np.array([base, pos], np.int32).reshape((-1, 2)))
                    base = pos
                    max_dist = 1

        if max_dist>rm_rest:
            pos=max_pos
            center = (base + pos) / 2
            drct = to_item_vec(pos - base) * (dist_thr[1] / 2)
            #print(pos, base)
            #print(np.linalg.norm(to_item_vec(pos - base),2), np.linalg.norm((center-drct) - (center+drct), 2))
            line_list.append(np.array([center-drct, center+drct], np.int32).reshape((-1, 2)))
            #line_list.append(np.array([base, pos], np.int32).reshape((-1, 2)))

    return line_list

def list2lines(line_list):
    return [Line(x[0,:], x[1,:]) for x in line_list]

def lines2list(line_list):
    return [np.vstack((x.p1, x.p2)) for x in line_list]

def rm_close_lines(line_list, angle_thr=np.deg2rad(15), dist_thr=40):
    idx=0
    while idx<len(line_list)-1:
        line_hold=line_list[idx]
        for line in line_list[idx+1:]:
            if (line_hold.angel_to(line)<angle_thr and line_hold.dist_to(line)<dist_thr) or line_hold.intersect_to(line):
                line_list.remove(line_hold)
                break
        else:
            idx+=1
    return line_list

def rm_close_lines2(line_list, dist_thr=(20,20)):
    idx=0
    while idx<len(line_list)-1:
        line_hold=line_list[idx]
        for line in line_list[idx+1:]:
            min_dist, rest_dist=line_hold.minr_rest_dist_to(line)
            if (min_dist<dist_thr[0] and rest_dist<dist_thr[1]) or line_hold.intersect_to(line):
                line_list.remove(line_hold)
                break
        else:
            idx+=1
    return line_list

def window_capture(filename):
    hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def makeVideo(path, frame_count, frame_getter, size=(1920,1080), fps = 30):
    # size = (1920, 1080)  # 需要转为视频的图片的尺寸，这里必须和图片尺寸一致
    video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)

    for idx in range(frame_count):
        print(idx)
        video.write(frame_getter(idx))

    video.release()
    cv2.destroyAllWindows()