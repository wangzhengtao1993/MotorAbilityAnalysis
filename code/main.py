# author:wzt
import pandas as pd
import os
import win32com.client as win32
#win32api找不到时 pip install pywin32==225

class EMGProcess(object):

    def __init__(self, folder):
        self.header = 4  # 表头在第四行
        self.folder = folder  # 文件夹路径
        print("Path:", folder)

    def save_as_high_ver(self):
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
                wb.SaveAs(self.folder + "\\Process\\" + file + "x", FileFormat=51)
                # FileFormat = 51 is for .xlsx extension
                # FileFormat = 56 is for .xls extension
                # print("%s has been saved as .xlsx" % file)
        wb.Close()
        excel.Application.Quit()
        print("All files have been saved as .xlsx")

        # print("将文件%s进行高版本转换" % file)
        # print(self.folder + '\\' + file)
        # wb = xw.Book(self.folder + '\\' + file)
        # wb.save(self.folder + '\\' + file_name + ".xlsx")

        # data = pd.DataFrame(pd.read_excel(self.folder + '\\' + file))  # 读取xls文件
        #
        # data.to_excel(self.folder + '\\' + file_name + '格式转变.xlsx', index=False)  # 格式转换

        # wb = xw.Book(self.path)
        # wb =

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

        # emg_data = self.read_emg()
        # # shape直接用的话表头上面不能有其他东西
        # print(emg_data.shape)


def main():
    print("debug")
    folder = r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406"
    EP = EMGProcess(folder)
    EP.run()


if __name__ == '__main__':
    main()
