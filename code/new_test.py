# author:wzt
from PySide2.QtWidgets import QApplication, QMessageBox, QDialog, QFileDialog
from PySide2.QtUiTools import QUiLoader
from pymysql import *
import os
import tkinter as tk
from tkinter import filedialog
import win32com.client as win32
from numpy import *
import pandas as pd


class NewTest(QDialog):
    """
    新建受试者信息并存入数据库
    """

    def __init__(self, user_id):
        super().__init__()
        self.debug = True
        self.user_id = user_id
        # 建立数据库连接
        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis', charset='utf8')
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")
        sql = "select * from t_user where user_id = %s" % self.user_id
        print("sql:", sql)
        self.cursor.execute(sql)
        self.user_info = self.cursor.fetchone()

        # 调用ui文件
        self.ui = QUiLoader().load('ui_design/t_file_cfg.ui')  # 路径用/，以免被认成转义，与系统用法不冲突
        self.ui.progressBar.setValue(0)  # 初始化进度条
        self.upper_directory = ""
        self.lower_directory = ""
        self.update_user_info()  # 初始化信息显示

        # 槽函数
        self.ui.upper_folder_btn.clicked.connect(self.get_upper_directory)  # 导入上肢文件夹
        self.ui.lower_folder_btn.clicked.connect(self.get_lower_directory)  # 导入下肢文件夹
        # 继承了QDialog，所以自带以下两个槽函数，ok和cancel
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.save_file_cfg()
        print("ok")
        # self.__del__()

    def reject(self):
        print("cancel")
        # self.__del__()

    @staticmethod
    def get_directory():
        # tk模块固定写法，打开文件夹对话框
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        # 替换斜杠，不然会报错
        directory = directory.replace("/", "\\")
        return directory

    def save_to_database(self):
        if self.debug:
            pass
        else:
            self.conn.commit()

    def get_upper_directory(self):
        # 1.更改标记，确定上下肢
        self.upper_limb_flag = True
        # 2. 获取文件夹路径
        self.upper_directory = self.get_directory()
        # 3.保存为高版本
        self.save_as_high_ver(self.upper_directory)
        # 4. 保存数据至数据库
        self.save_emg_to_database(self.upper_directory)
        # 5. 更新显示
        self.update_user_info()

    def get_lower_directory(self):
        self.upper_limb_flag = False
        self.lower_directory = self.get_directory()
        self.save_as_high_ver(self.lower_directory)
        self.save_emg_to_database(self.lower_directory)
        self.update_user_info()

    def update_user_info(self):
        if self.upper_directory and self.lower_directory == "":
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s已导入\n下肢文件夹：%s未导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_directory,
                                           self.lower_directory))
            self.ui.progressBar.setValue(100)
        elif self.lower_directory and self.upper_directory == "":
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s未导入\n下肢文件夹：%s已导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_directory,
                                           self.lower_directory))
            self.ui.progressBar.setValue(100)
        elif self.lower_directory and self.upper_directory:
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s已导入\n下肢文件夹：%s已导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_directory,
                                           self.lower_directory))
            self.ui.progressBar.setValue(100)
        else:
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s未导入\n下肢文件夹：%s未导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_directory,
                                           self.lower_directory))

    def save_as_high_ver(self, directory):
        """
        源文件格式错误，另存为xlsx
        """
        # 1.创建子文件夹储存数据
        process_directory = directory + r"/Process/"
        if os.path.exists(process_directory):
            print("process folder exists")
        else:
            os.mkdir(process_directory)
            print("process folder created")
        file_list = os.listdir(process_directory)
        # 2.判断文件是否已经转换
        if len(file_list) > 0:
            self.ui.progressBar.setValue(100)
            print("文件已转换")
        else:
            # 1.获得当前目录下所有文件名
            file_list = os.listdir(directory)
            file_num = len(file_list)
            file_done_number = 0
            # 2.打开excel处理程序，固定写法
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            # excel.Application.Visible = False
            print("saving as .xlsx")
            for file in file_list:
                file_done_number += 1
                self.ui.progressBar.setValue(file_done_number / file_num * 100)
                # 将文件名与后缀分开
                file_name, suff = os.path.splitext(file)
                if suff == ".xls":
                    wb = excel.Workbooks.Open(directory + r"/" + file)
                    # wb.Application.Visible = False
                    # print("debug", process_folder + file + "x")
                    new_file_path = directory + r"/Process/" + file + "x"
                    wb.SaveAs(new_file_path, FileFormat=51)
                    # FileFormat = 51 is for .xlsx extension
                    # FileFormat = 56 is for .xls extension
                    print("%s has been saved as .xlsx" % file)
                    wb.Close()
            excel.Application.Quit()
            log_info = "All files have been saved as .xlsx\n"
            self.rename_test_file(process_directory)
            print(log_info)
            directory = directory + r"/Process/"
            self.create_log(directory, log_info)

    def rename_test_file(self, process_directory):
        # 1.获得文件名
        file_list = os.listdir(process_directory)
        f = file_list[2] # 为防止得到log文件名，所以选序号大于0的文件
        print(f[0:26])
        # 2.从数据库获得文件编号表

        sql = """SELECT * FROM `t_file_cfg` WHERE `user_id` = '%s'""" % self.user_id
        self.cursor.execute(sql)
        self.user_info = self.cursor.fetchone()

        # file_name = pd.read_excel(self.subject, dtype=str)
        # print(file_name)
        #
        # # 遍历所有文件
        # if self.upper_limb:
        #     motion_id_start = 0
        #     motion_id_end = 7
        # else:
        #     motion_id_start = 7
        #     motion_id_end = 14
        #
        # keyword = "Odau"
        # for file in file_list:
        #     if "new_name.txt" in file_list:
        #         print("已重命名")
        #         break
        #     else:
        #         if keyword in file:
        #             print("file", file[-15:-12])
        #             file_id = file[-15:-12]
        #             # 遍历所有文件id
        #             for motion in range(motion_id_start, motion_id_end):
        #                 for motion_pattern in range(1, 4):
        #                     # print("motion:", motion)
        #                     # print("motion_pattern:", motion_pattern)
        #                     motion_id = file_name.iloc[motion, motion_pattern]
        #                     # print("motion_id:", motion_id)
        #                     if file_id == motion_id:
        #                         dst_name = f[:-15] + file_name.iloc[motion, motion_pattern] + "_Odau_1" + \
        #                                    file_name.columns[motion_pattern] + file_name.iloc[motion, 0] + ".xlsx"
        #                         self.log_create("new_name", dst_name + "\n")
        #
        #                         if os.path.exists(self.process_folder + file):
        #                             os.rename(self.process_folder + file, self.process_folder + dst_name)
        #                             print("rename:", dst_name)
        #                         else:
        #                             pass

    def save_file_cfg(self):
        motion = ["", "", ""]
        for j in range(0, 14):
            for i in range(0, 3):
                temp = self.ui.t_file_cfg.item(j, i).text()
                motion[i] = temp
            header = self.ui.t_file_cfg.verticalHeaderItem(j).text()
            file_cfg = [self.user_id, header] + motion

            sql = """INSERT INTO t_file_cfg (user_id, motion, active, mvc, passive) 
            VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, file_cfg)
        self.save_to_database()

    def get_table_name(self):
        pass

    def save_emg_to_database(self, folder):
        path = folder + r"/Process/"
        log_path = path + "log.txt"
        log_info = open(log_path, "r").readlines()
        flag = False
        for data in log_info:
            if data == "raw emg have been saved to database\n":
                flag = True
                print("raw emg have been saved to database")
                break

        if not flag:
            print("saving")
            self.get_raw_emg(path)
            msg = "raw emg have been saved to database\n"
            self.create_log(folder + r"/Process/", msg)

    def get_raw_emg(self, path):
        keyword = "Odau"
        file_list = os.listdir(path)
        file_num = len(file_list)
        file_done_number = 0

        for file in file_list:
            file_done_number += 1
            self.ui.progressBar.setValue(file_done_number / file_num * 100)
            if keyword in file:
                test_time = file[0:26]
                print("test_time", test_time)
                data = pd.read_excel(path + file, header=4)
                frame_num = len(data)
                print("frame_num:", frame_num)
                data["time"] = data["Frame"] / 1000
                for i in range(1, 7):
                    EMG = ("EMG_" + str(i))
                    analog = ("Analog_" + str(i))
                    column = data[analog]
                    emg_mean = column.mean()
                    data[EMG] = (data[analog] - emg_mean) / 2  # 除以500倍，×1000，mV

                sql = """INSERT INTO t_emg_upper 
                (test_time,user_id, frame,time,emg_1,emg_2,emg_3,emg_4,emg_5,emg_6) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                #
                for r in range(0, frame_num):
                    print(r)
                    frame = int(data["Frame"][r])
                    time = float(data["time"][r])
                    emg_1 = float(data["EMG_1"][r])
                    emg_2 = float(data["EMG_2"][r])
                    emg_3 = float(data["EMG_3"][r])
                    emg_4 = float(data["EMG_4"][r])
                    emg_5 = float(data["EMG_5"][r])
                    emg_6 = float(data["EMG_6"][r])

                    values = (test_time, int(self.user_id), frame, time, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6)
                    # 执行sql语句

                    self.cursor.execute(sql, values)
                self.save_to_database()

    @staticmethod
    def create_log(directory, info):
        full_path = directory + "log" + '.txt'
        file = open(full_path, 'a')
        file.write(info)


if __name__ == '__main__':
    user_id = 1
    app = QApplication([])
    new_test = NewTest(1)
    new_test.ui.show()
    new_test.ui.exec_()
