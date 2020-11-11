# author:wzt
from PySide2.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from pymysql import *
import os
import tkinter as tk
from tkinter import filedialog
import win32com.client as win32
from numpy import *
import pandas as pd
from EMGProcess import EMGProcess as ep


class NewTest(QDialog):
    """
    新建受试者信息并存入数据库
    """

    def __init__(self, user_id):
        super().__init__()
        self.debug = False
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
        self.set_file_cfg()  # 若file_cfg存在则显示，若不存在则显示为空

        # 槽函数
        self.ui.upper_folder_btn.clicked.connect(self.get_upper_directory)  # 导入上肢文件夹
        self.ui.lower_folder_btn.clicked.connect(self.get_lower_directory)  # 导入下肢文件夹
        # 继承了QDialog，所以自带以下两个槽函数，ok和cancel
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.save_file_cfg()
        print("ok")

    def reject(self):
        print("cancel")

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

    @staticmethod
    def get_directory():
        # tk模块固定写法，打开文件夹对话框
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        # 替换斜杠，不然会报错
        directory = directory.replace("/", "\\")
        return directory

    def get_file_id(self, motion_name, motion_mode):
        # 从表t_file_cfg中选择motion_name 和 motion_mode对应的文件名
        sql = """SELECT %s FROM `t_file_cfg` WHERE (`user_id` = '%s' and motion = '%s') """ \
              % (motion_mode, self.user_id, motion_name)
        self.cursor.execute(sql)
        file_id = self.cursor.fetchone()[0]  # 返回元组，加[0]取值
        return file_id

    def set_file_cfg(self):

        sql = """SELECT * from t_file_cfg WHERE user_id = %s """ % self.user_id
        self.cursor.execute(sql)
        file_id = self.cursor.fetchall()
        if file_id:
            self.ui.l_file_cfg.setText("文件定义已存在")
            print(file_id)
            for j in range(0, 14):
                for i in range(0, 3):
                    # 读取表格中的信息，一次存一行
                    temp = file_id[j][i + 3]
                    self.ui.t_file_cfg.setItem(j, i, QTableWidgetItem(temp))
        else:
            pass

    def save_file_cfg(self):
        file_id = ["", "", ""]
        for j in range(0, 14):
            for i in range(0, 3):
                # 读取表格中的信息，一次存一行
                temp = self.ui.t_file_cfg.item(j, i).text()
                file_id[i] = temp
            motion_name = self.ui.t_file_cfg.verticalHeaderItem(j).text()
            file_cfg = [self.user_id, motion_name] + file_id

            sql = """INSERT INTO t_file_cfg (user_id, motion, active, mvc, passive) 
            VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, file_cfg)
        self.save_to_database()

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
        # self.save_emg_to_database(self.upper_directory)
        # 5. 更新显示
        self.update_user_info()

    def get_lower_directory(self):
        self.upper_limb_flag = False
        self.lower_directory = self.get_directory()
        self.save_as_high_ver(self.lower_directory)
        # self.save_emg_to_database(self.lower_directory)
        self.update_user_info()

    def save_as_high_ver(self, directory):
        """
        源文件格式错误，另存为.xlsx
        :param directory: 数据文件夹
        """
        # 1.创建子文件夹储存数据
        process_directory = directory + r"/Process/"
        if os.path.exists(process_directory):
            print("process folder exists")
        else:
            os.mkdir(process_directory)
            self.create_log(process_directory, "")
            print("process folder created")
        file_list = os.listdir(process_directory)
        # 2.判断文件是否已经转换
        log_info = "All files have been saved as .xlsx\n"
        if self.read_log(process_directory, log_info):
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
                print("progress:", file_done_number / file_num * 20)
                self.ui.progressBar.setValue(file_done_number / file_num * 20)
                # 将文件名与后缀分开
                file_name, suff = os.path.splitext(file)
                if suff == ".xls":
                    wb = excel.Workbooks.Open(directory + r"/" + file)
                    new_file_path = directory + r"/Process/" + file + "x"
                    wb.SaveAs(new_file_path, FileFormat=51)
                    # FileFormat = 51 is for .xlsx extension
                    # FileFormat = 56 is for .xls extension
                    print("%s has been saved as .xlsx" % file)
                    wb.Close()
            excel.Application.Quit()
            print(log_info)
            directory = directory + r"/Process/"
            self.create_log(directory, log_info)
        # 重命名
        print("debug")
        self.rename_test_file(process_directory)

    def rename_test_file(self, process_directory):
        """
        重命名文件并将文件保存至数据库
        :param process_directory:
        """
        # 1. 判断是否重命名
        log_info = "all files have been renamed\nraw emg data has been saved in database\n"
        if not self.read_log(process_directory, log_info):
            # 2.获得文件列表
            file_list = os.listdir(process_directory)
            file_num = len(file_list)
            file_done_number = 0
            # 3.从数据库获得文件编号表
            if self.upper_limb_flag:
                motion_name_list = ["上肢静息", "屈肩", "伸肩", "屈肘", "伸肘", "屈腕", "伸腕"]
            else:
                motion_name_list = ["下肢静息", "屈髋", "伸髋", "屈膝", "伸膝", "踝背伸", "踝跖屈"]
            motion_mode_list = ["active", "MVC", "passive"]

            for motion_name in motion_name_list:
                for motion_mode in motion_mode_list:
                    file_id = self.get_file_id(motion_name, motion_mode)
                    print(motion_mode, motion_name, file_id)
                    # 4.重命名
                    for file in file_list:
                        # print("file", file[-15:-12])
                        dst_file_id = self.get_file_id(motion_name, motion_mode)
                        # print(motion_mode, motion_name, file_id)
                        keyword = "_" + dst_file_id + "_"
                        file_name, suff = os.path.splitext(file)
                        file_done_number += 1
                        self.ui.progressBar.setValue(file_done_number / file_num * 80 + 20)
                        if keyword in file_name:
                            dst_file_name = file_name + "_" + motion_mode + "_" + motion_name + suff
                            if os.path.exists(process_directory + file):
                                os.rename(process_directory + file, process_directory + dst_file_name)
                                renamed_file = process_directory + dst_file_name
                                print("rename:", dst_file_name)
                                """ 保存数据至数据库 """
                                self.save_emg_to_database(renamed_file, motion_mode, motion_name)
                            else:
                                pass
            # 5.创建日志
            self.ui.progressBar.setValue(100)
            print(log_info)
            self.create_log(process_directory, log_info)
        else:
            pass

    def save_emg_to_database(self, renamed_file, motion_mode, motion_name):
        # 1.判断是否为肌电信号文件
        keyword = "Odau"
        if keyword in renamed_file:
            # 2.获得测试时间
            directory, file_name = os.path.split(renamed_file)
            test_time = file_name[0:26]
            # 3.生成表名
            motion_name_dic = {"上肢静息": "_rest_upper",
                               "下肢静息": "_rest_lower",
                               "屈肩": "_shoulder_flexion",
                               "伸肩": "_shoulder_extension",
                               "屈肘": "_elbow_flexion",
                               "伸肘": "_elbow_extension",
                               "屈腕": "_wrist_flexion",
                               "伸腕": "_wrist_extension",
                               "屈髋": "_hip_flexion",
                               "伸髋": "_hip_extension",
                               "屈膝": "_knee_flexion",
                               "伸膝": "_knee_extension",
                               "踝背伸": "_ankle_flexion",
                               "踝跖屈": "_ankle_extension",
                               }
            if motion_name == "上肢静息":
                table_name = "t_emg_rest_upper"
            elif motion_name == "下肢静息":
                table_name = "t_emg_rest_lower"
            else:
                table_name = "t_emg_" + motion_mode + motion_name_dic[motion_name]
            # 4. 生成SQL语句，INSERT IGNORE INTO若数据存在，不重复导入
            sql = "INSERT IGNORE INTO " + table_name + """(test_time,user_id, frame,time,emg_1,emg_2,emg_3,emg_4,emg_5,emg_6) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            print(sql)
            # 5.读取数据
            data = pd.read_excel(renamed_file, header=4)
            frame_num = len(data)
            data["time"] = data["Frame"] / 1000
            for i in range(1, 7):
                EMG = ("EMG_" + str(i))
                analog = ("Analog_" + str(i))
                column = data[analog]
                emg_mean = column.mean()
                data[EMG] = (data[analog] - emg_mean) / 2  # 除以500倍，×1000，mV

            # 6. 生成写入数据库的数据
            for r in range(0, frame_num):
                frame = int(data["Frame"][r])
                time = float(data["time"][r])
                emg_1 = float(data["EMG_1"][r])
                emg_2 = float(data["EMG_2"][r])
                emg_3 = float(data["EMG_3"][r])
                emg_4 = float(data["EMG_4"][r])
                emg_5 = float(data["EMG_5"][r])
                emg_6 = float(data["EMG_6"][r])
                # rms_1 = ep.rms(emg_1)
                # print(rms_1)

                values = (test_time, int(self.user_id), frame, time, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6)
                # 7.执行sql语句，导入数据
                self.cursor.execute(sql, values)


            # 8. 执行commit()，保存数据
            self.save_to_database()
        else:
            pass



    @staticmethod
    def create_log(directory, log_info):
        full_path = directory + "log" + '.txt'
        file = open(full_path, 'a')
        file.write(log_info)

    @staticmethod
    def read_log(directory, log_info):
        log_path = directory + "log.txt"
        all_log_info = open(log_path, "r").readlines()
        print("debug", all_log_info)
        if log_info in all_log_info:
            print(log_info)
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication([])
    new_test = NewTest(1)
    new_test.ui.show()
    new_test.ui.exec_()
