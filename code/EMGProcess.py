# author:wzt

from numpy import *
import numpy as np
import pandas as pd
from pymysql import *


class EMGProcess(object):

    def __init__(self, motion_info):
        self.win_set = [100, 100]
        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis', charset='utf8')
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")

    # def get_data(self):
    #     """
    #     从数据库获取一列emg值
    #     :param emg_id: 输入需要获取的emg信号表头
    #     :return: 返回一组raw_emg值
    #     """
    #     user_id = self.motion_info[0]
    #     t_motion = self.motion_info[2]
    #     emg_id = self.motion_info[3]
    #     sql = "select %s from %s where user_id = %s" % (emg_id, t_motion, user_id)
    #     print("sql:", sql)
    #     self.cursor.execute(sql)
    #     raw_emg = self.cursor.fetchall()
    #     frames_num = len(raw_emg)
    #     emg = zeros(frames_num, dtype=float)
    #     for i in range(frames_num):
    #         emg[i] = raw_emg[i][0]
    #     return emg

    # @staticmethod
    # def output(array):
    #     for i in range(len(array)):
    #         for j in range(len(array[0])):
    #             print(array[i][j], end='')
    #             print('   ', end='')
    #         print(' ')

    @staticmethod
    def emg_mean(column):
        return column.mean()

    @staticmethod
    def rect(raw):
        return np.fabs(raw)

    @staticmethod
    def rms(raw):
        sw = EMGProcess.slid_window(raw)
        frame, width = shape(sw)
        RMS = zeros(frame, dtype=float)
        for j in range(0, frame):
            rms_p = 0
            for k in range(0, width):
                rms_p = rms_p + sw[j][k] ** 2  # 平方和
            RMS[j] = (rms_p / width) ** 0.5  # 开方
        return RMS

    @staticmethod
    def slid_window(raw):
        # 一次传入re_raw的一列
        length = len(raw)
        step = 100
        width = 100
        frame = int((length - width) / step + 1)  # 处理后的帧数
        sw = zeros((frame, width), dtype=float)  # 初始化矩阵，每行是一个时间窗
        i = 0
        while i < length - width + 1:
            # 每行新建空数组，作为window
            window = array([])
            for j in range(0, width):
                # 每列从i添加到i+width
                window = append(window, raw[i + j])
            # 生成sw矩阵
            sw[int(i / step)] = window
            i += step
        return sw

    def max_mean(self):
        keyword = "Odau"
        file_list = os.listdir(self.process_folder)
        for file in file_list:
            if "rms.txt" in file_list:
                print("已绘图")
                break
            else:
                if keyword in file:
                    print(file)
                    data = pd.read_excel(self.process_folder + file, sheet_name="RMS")
                    if self.upper_limb:
                        col = {1: "RMS_1_三角肌前束",
                               2: "RMS_2_三角肌后束",
                               3: "RMS_3_肱二头肌",
                               4: "RMS_4_肱三头肌",
                               5: "RMS_5_桡侧腕屈肌",
                               6: "RMS_6_尺侧腕伸肌"}

                    else:
                        col = {1: "RMS_1_股直肌",
                               2: "RMS_2_股二头肌",
                               3: "RMS_3_半腱肌",
                               4: "RMS_4_股内侧肌",
                               5: "RMS_5_胫骨前肌",
                               6: "RMS_6_外侧腓肠肌"
                               }
                    # ["time", "RMS_1_股直肌", "RMS_2_股二头肌", "RMS_3_半腱肌", "RMS_4_股内侧肌", "RMS_5_胫骨前肌", "RMS_6_外侧腓肠肌"]

                    # 取最大的前40%的值，求平均
                    frames = len(data)
                    max_frames = int(0.1 * frames)
                    rms_max = ["RMS_max", 0, 0, 0, 0, 0, 0]

                    for i in range(1, 7):
                        temp = data.iloc[data[col[i]].argsort()[-max_frames:]]
                        # print("debug1",temp)
                        rms_max[i] = mean(temp[col[i]])

                        # print("debug2", rms_max)
                    print(rms_max)


if __name__ == '__main__':
    win_set = [100, 100]
    ep = EMGProcess(win_set)
    user_id = 1
    emg_id = "emg_1"
    t_motion = "t_emg_mvc_ankle_extension"

    emg = ep.get_raw_emg(1, emg_id, t_motion)
    print(emg)
