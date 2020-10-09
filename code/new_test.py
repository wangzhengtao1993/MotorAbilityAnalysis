# author:wzt
from PySide2.QtWidgets import QApplication, QMessageBox, QDialog, QFileDialog
from PySide2.QtUiTools import QUiLoader
from pymysql import *
import tkinter as tk
from tkinter import filedialog
import os
import win32com.client as win32
from numpy import *
import time
from main import EMGProcess




class NewTest(QDialog):
    """
    新建受试者信息并存入数据库
    """

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis', charset='utf8')
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")
        # 调用ui文件
        self.ui = QUiLoader().load('ui_design/t_file_cfg.ui')  # 路径用/，以免被认成转义，与系统用法不冲突

        sql = "select * from t_user where user_id = %s" % self.user_id
        print("sql:", sql)
        self.cursor.execute(sql)
        self.user_info = self.cursor.fetchone()
        self.upper_folder = ""
        self.lower_folder = ""
        self.update_user_info()
        self.ui.upper_folder_btn.clicked.connect(self.get_upper_folder)
        self.ui.lower_folder_btn.clicked.connect(self.get_lower_folder)
        # 继承了QDialog，所以自带以下两个槽函数
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.progressBar.setValue(0)

    # def __del__(self):
    #     self.cursor.close()
    #     self.conn.close()
    #     print("database motor_ability_analysis disconnected")

    def accept(self):
        self.save()
        print("ok")
        self.__del__()

    def reject(self):
        print("cancel")
        self.__del__()

    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        directory = directory.replace("/", "\\")

        return directory

    def get_upper_folder(self):
        self.upper_folder = self.get_path()
        self.save_as_high_ver(self.upper_folder)
        self.update_user_info()

    def get_lower_folder(self):
        self.lower_folder = self.get_path()
        self.save_as_high_ver(self.lower_folder)
        self.update_user_info()

    def update_user_info(self):
        if self.upper_folder and self.lower_folder == "":
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s已导入\n下肢文件夹：%s未导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_folder, self.lower_folder))
            self.ui.progressBar.setValue(100)
        elif self.lower_folder and self.upper_folder == "":
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s未导入\n下肢文件夹：%s已导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_folder, self.lower_folder))
            self.ui.progressBar.setValue(100)
        elif self.lower_folder and self.upper_folder:
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s已导入\n下肢文件夹：%s已导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_folder, self.lower_folder))
            self.ui.progressBar.setValue(100)
        else:
            self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s未导入\n下肢文件夹：%s未导入"
                                        % (self.user_info[0], self.user_info[1], self.upper_folder, self.lower_folder))




    def save_as_high_ver(self, path):
        """
        源文件格式错误，另存为xlsx
        """
        process_folder = path + r"/Process/"
        print(process_folder)
        if os.path.exists(process_folder):
            print("process folder exists")
        else:
            os.mkdir(process_folder)
            print("process folder created")

        file_list = os.listdir(process_folder)


        if len(file_list) > 0:
            print("文件已转换")
        else:
            # 1.获得当前目录下所有文件名
            file_list = os.listdir(path)
            file_num = len(file_list)
            file_done_number = 0
            # 2.打开excel处理程序，固定写法
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            # excel.Application.Visible = False
            print("saving as .xlsx")
            for file in file_list:
                file_done_number  += 1
                print(file_done_number)
                self.ui.progressBar.setValue(file_done_number/file_num*100)

                # 将文件名与后缀分开
                file_name, suff = os.path.splitext(file)
                if suff == ".xls":
                    wb = excel.Workbooks.Open(path + r"/" + file)
                    # wb.Application.Visible = False
                    # print("debug", process_folder + file + "x")
                    new_file_path = path + r"/Process/" + file + "x"
                    wb.SaveAs(new_file_path, FileFormat=51)
                    # FileFormat = 51 is for .xlsx extension
                    # FileFormat = 56 is for .xls extension
                    print("%s has been saved as .xlsx" % file)
            wb.Close()
            excel.Application.Quit()
            print("All files have been saved as .xlsx")


    def save(self):
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
        # self.conn.commit()



if __name__ == '__main__':
    user_id = 1
    app = QApplication([])
    new_test = NewTest(1)
    new_test.ui.show()
    new_test.ui.exec_()
