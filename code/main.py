# author:wzt
import pandas as pd
import os
import win32com.client as win32

from numpy import *
import openpyxl


# win32api找不到时 pip install pywin32==225

class EMGProcess(object):

    def __init__(self, folder):
        self.header = 4  # 表头在第四行
        self.folder = folder  # 文件夹路径
        self.process_folder = self.folder + "\\Process\\"
        self.win_set = (100, 100)
        print("Path:", folder)

    def save_as_high_ver(self):
        """
        源文件格式错误，另存为xlsx
        """
        file_list = os.listdir(self.process_folder)
        if len(file_list) > 0:
            print("文件已转换")
        else:
            # 1.获得当前目录下所有文件名
            file_list = os.listdir(self.folder)
            # 2.打开excel处理程序，固定写法
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            print("saving as .xlsx")
            for file in file_list:
                # 将文件名与后缀分开
                file_name, suff = os.path.splitext(file)
                if suff == ".xls":
                    wb = excel.Workbooks.Open(self.folder + "\\" + file)
                    wb.SaveAs(self.process_folder + file + "x", FileFormat=51)
                    # FileFormat = 51 is for .xlsx extension
                    # FileFormat = 56 is for .xls extension
                    print("%s has been saved as .xlsx" % file)
            wb.Close()
            excel.Application.Quit()
            print("All files have been saved as .xlsx")

    def new_columns(self):
        keyword = "Odau"
        file_list = os.listdir(self.process_folder)
        for file in file_list:
            if "log.txt" in file_list:
                print("列已添加")
                break
            else:
                if keyword in file:
                    print(file)
                    wb = openpyxl.load_workbook(self.process_folder + file)  # 打开文件
                    sheet_1 = wb.sheetnames[0]  # 获得第一个sheet名
                    data = pd.read_excel(self.process_folder + file, header=4)
                    print("新建肌电信号列")
                    data["Frame"] = data["Frame"] / 1000
                    data.rename(columns={"Frame": "time"}, inplace=True)
                    print("Data:", data)
                    for i in range(1, 7):
                        EMG = ("EMG_" + str(i))
                        analog = ("Analog_" + str(i))
                        column = data[analog]
                        emg_mean = self.emg_mean(column)
                        data[EMG] = (data[analog] - emg_mean) / 2  # 除以500倍，×1000，mV
                    print("新建工作表RMS")

                    rms_data = pd.DataFrame()
                    for i in range(1, 7):
                        EMG_ = ("EMG_" + str(i))
                        RMS_ = ("RMS_" + str(i))
                        print("debug")
                        emg_rms_temp = self.RMS(data[EMG_])
                        print("temp:", emg_rms_temp)
                        rms_data[RMS_] = emg_rms_temp

                    frames = shape(rms_data)[0]
                    end_time = frames * self.win_set[0] / 1000
                    print("end_time", end_time)
                    time = arange(0, end_time, self.win_set[0] / 1000)
                    print("time:", time)

                    df_rms = pd.DataFrame({"time": time,
                                           "RMS_1": rms_data['RMS_1'],
                                           "RMS_2": rms_data['RMS_2'],
                                           "RMS_3": rms_data['RMS_3'],
                                           "RMS_4": rms_data['RMS_4'],
                                           "RMS_5": rms_data['RMS_5'],
                                           "RMS_6": rms_data['RMS_6'],
                                           })
                    # frames = shape(df_rms)
                    #
                    # df_rms.insert(0, "time", zeros(frames))
                    # 分别写入两张表
                    writer = pd.ExcelWriter(self.process_folder + file)
                    data.to_excel(writer, sheet_name=sheet_1, index=False)
                    df_rms.to_excel(writer, sheet_name="RMS", index=False)
                    writer.save()

        self.log_create("log")

    def log_create(self, name):
        full_path = self.process_folder + name + '.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        file.write("新建列")

    def read_emg(self, path):
        return pd.read_excel(path, header=self.header)

    @staticmethod
    def emg_mean(column):
        return column.mean()

    @staticmethod
    def rect(raw):
        return np.fabs(raw)

    # 滑动时间窗
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

    def AEMG(self, re_raw):
        l = len(re_raw)
        s = self.win_set[0]
        w = self.win_set[1]
        c = int((l - w) / s + 1)  # 处理后的帧数
        AEMG = zeros((c, 17), dtype=float)
        for j in range(0, c):
            AEMG[j][0] = re_raw[int(j * s + s / 2)][0]
        # print('t:', AEMG[:,0])
        for i in range(1, 9):
            sw = self.slidwindow(re_raw[:, i], win_set)
            for j in range(0, c):
                AEMG[j][i] = mean(sw[j, :])
        print('last AEMG:', AEMG[c - 1][16])
        return AEMG

    def run(self):
        # 1.另存为高版本
        self.save_as_high_ver()
        # 2.肌电信号预处理，矫正零偏，计算RMS
        self.new_columns()


def main():
    folder = r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406"
    EP = EMGProcess(folder)
    EP.run()


if __name__ == '__main__':
    main()
