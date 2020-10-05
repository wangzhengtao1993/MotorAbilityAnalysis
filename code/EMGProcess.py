# author:wzt

from numpy import *
import re
import numpy as np
import pandas as pd
import win32ui


class readData():
    FREQUENCY = 0
    TESTTIME = 0
    raw_EMG = []
    raw = []
    re_raw = []
    RMS = []
    AEMG = []
    MOTION = []

    def __init__(self):
        # 0代表另存为对话框，1代表打开文件对话框
        dlg = win32ui.CreateFileDialog(1)
        # 默认目录
        dlg.SetOFNInitialDir('C:/')
        # 显示对话框
        dlg.DoModal()
        # 获取用户选择的文件全路径
        filename = dlg.GetPathName()
        self.getMotion(filename)
        self.getTesttime(filename)
        self.getFrequency(filename)
        self.getRawEMG(filename)
        self.rect(self.raw)
        # self.RMS(self.sw)
        # self.slidwindow(self.re_raw)


    def getMotion(self,filename):
        Motion = int(re.sub("\D", "", filename))
        motion = ['','肩关节前屈', '肩关节外展', '是肘关节屈伸', '腕关节屈伸', '手指屈伸']
        self.MOTION = motion[Motion]
        print('Motion:', motion[Motion])
        return self.MOTION
    #获得测试时间及频率
    def getTesttime(self,filename):
        file = open(filename, mode='r', encoding='utf-8-sig')
        TESTDATE = file.readlines()[3]
        TESTDATE = re.sub("\D", "", TESTDATE)  # 测试时间
        TESTTIME = TESTDATE[4:8] + '-' + TESTDATE[2:4] + '-' + TESTDATE[0:2] + \
                   ' ' + TESTDATE[8:10] + ':' + TESTDATE[10:12] + ':' + TESTDATE[12:16]
        self.TESTTIME = TESTTIME
        file.close()
        print('debug')
        return self.TESTTIME
    #获得采样频率
    def getFrequency(self,filename):
        file = open(filename, mode='r', encoding='utf-8-sig')
        FREQUENCY = file.readlines()[2]
        FREQUENCY = int(re.sub("\D", "", FREQUENCY))  # 提取频率
        self.FREQUENCY = FREQUENCY
        file.close()
        return self.FREQUENCY
    #获得原始数据
    def getRawEMG(self,filename):
        testData = []
        c = 0
        with open(filename, mode='r', encoding='utf-8-sig') as txtData:
            lines = txtData.readlines()[5:]#从第5行开始逐行读
            frames = len(lines) #获得总帧数
            raw = zeros((frames,17), dtype=float) #初始化零矩阵帧数行，17列
            raw_row = 0
            for line in lines:
                lineData = line.strip('\n').split('\t')
                raw[raw_row] = lineData[:] #调用整行
                raw_row += 1
            # print('raw[1]:', raw[1])
            self.raw = raw
        return self.raw
    #整流
    def rect(self,raw):
        self.re_raw = np.fabs(raw)
        return self.re_raw
    #滑动时间窗
    def slidwindow(self,re_raw,win_set):
        #一次传入re_raw的一列
        l = len(re_raw)
        s = win_set[0]
        w = win_set[1]
        c = int((l - w) / s + 1)#处理后的帧数
        sw = zeros((c, w), dtype=float)  # 初始化矩阵，每行是一个时间窗
        i = 0
        while i < l - w + 1:
            window = array([])
            for j in range(0, w):
                window = np.append(window, re_raw[i + j])
            sw[int(i / s)] = window
            i += s
        self.sw = sw
        return self.sw
    #均方根
    def RMS(self,re_raw,win_set):
        l = len(re_raw)
        s = win_set[0]
        w = win_set[1]
        c = int((l - w) / s + 1)  # 处理后的帧数
        RMS = zeros((c, 17), dtype=float)
        for j in range(0, c):
            RMS[j][0] = re_raw[int(j * s)][0]
        for i in range(1, 17):
            sw = self.slidwindow(re_raw[:, i], win_set)
            for j in range(0, c):
                rms_p = 0
                for k in range(0,w):
                    rms_p = rms_p + sw[j][k] ** 2
                RMS[j][i] = (rms_p/w)**0.5
        return RMS

    def AEMG(self,re_raw,win_set):
        l = len(re_raw)
        s = win_set[0]
        w = win_set[1]
        c = int((l - w) / s + 1)#处理后的帧数
        AEMG = zeros((c, 17), dtype=float)
        for j in range(0,c):
            AEMG[j][0] = re_raw[int(j * s+s/2)][0]
        # print('t:', AEMG[:,0])
        for i in range(1,9):
            sw = self.slidwindow(re_raw[:,i],win_set)
            for j in range(0,c):
                AEMG[j][i] = mean(sw[j,:])
        print('last AEMG:',AEMG[c-1][16])
        return AEMG
        # print(AEMG)
