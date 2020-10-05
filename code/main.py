# author:wzt
import pandas as pd
import os
import win32com.client as win32
#win32api找不到时 pip install pywin32==225

class EMGProcess(object):

    def __init__(self, folder):
        self.header = 4  # 表头在第四行
        self.folder = folder  # 文件夹路径
        self.process_folder = self.folder + "\\Process\\"
        print("Path:", folder)

    def save_as_high_ver(self):
        file_list = os.listdir(self.process_folder)
        if len(file_list)>0:
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
                    data = pd.read_excel(self.process_folder+file, header=4)
                    print(data.columns)
                    print("新建肌电信号列")
                    for i in range(1, 7):
                        EMG = ("EMG_" + str(i))
                        data[EMG] = None
                    print("新建RMS列")
                    for i in range(1, 7):
                        RMS = ("RMS_" + str(i))
                        data[RMS] = None
                    data = data.set_index("Frame")
                    data.to_excel(self.process_folder+file)
        self.log_create("new")

    def log_create(self,name):
        full_path = self.process_folder + name + '.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        file.write("新建列")


    def read_emg(self, path):
        return pd.read_excel(path, header=self.header)

    def preprocessing(self):
        pass
        # 1. 读取数据
        # emg_data  = read_emg()
        # 2. 新建sheet，除以倍率，analog_3归零

    def run(self):
        # 1.另存为高版本
        self.save_as_high_ver()
        # 2.肌电信号预处理
        self.new_columns()

        # emg_data = self.read_emg()
        # # shape直接用的话表头上面不能有其他东西
        # print(emg_data.shape)


def main():
    folder = r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406"
    EP = EMGProcess(folder)
    EP.run()


if __name__ == '__main__':
    main()
