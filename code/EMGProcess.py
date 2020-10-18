# author:wzt

from numpy import *
import numpy as np
import pandas as pd


class EMGProcess(object):
    class EMGProcess(object):

        def __init__(self, win_set):
            self.win_set = win_set  # 滑动时间窗

        @staticmethod
        def output(array):
            for i in range(len(array)):
                for j in range(len(array[0])):
                    print(array[i][j], end='')
                    print('   ', end='')
                print(' ')

        @staticmethod
        def emg_mean(column):
            return column.mean()

        @staticmethod
        def rect(raw):
            return np.fabs(raw)

        def RMS(self, raw):
            sw = self.slid_window(raw)
            frame, width = shape(sw)
            RMS = zeros(frame, dtype=float)
            for j in range(0, frame):
                rms_p = 0
                for k in range(0, width):
                    rms_p = rms_p + sw[j][k] ** 2  # 平方和
                RMS[j] = (rms_p / width) ** 0.5  # 开方
            return RMS

        def slid_window(self, raw):
            # 一次传入re_raw的一列
            length = len(raw)
            step = self.win_set[0]
            width = self.win_set[1]
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


