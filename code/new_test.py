# author:wzt
from PySide2.QtWidgets import QApplication, QMessageBox, QDialog
from PySide2.QtUiTools import QUiLoader
from pymysql import *
import tkinter as tk
from tkinter import filedialog
from numpy import zeros


class NewTest(QDialog):
    """
    新建受试者信息并存入数据库
    """

    def __init__(self, user_id):
        super().__init__()

        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis', charset='utf8')
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")
        # 调用ui文件
        self.ui = QUiLoader().load('ui_design/t_file_cfg.ui')  # 路径用/，以免被认成转义，与系统用法不冲突

        sql = "select * from t_user where user_id = %s" % user_id
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

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print("database motor_ability_analysis disconnected")

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
        path = filedialog.askdirectory()
        return path

    def get_upper_folder(self):
        self.upper_folder = self.get_path()
        self.update_user_info()

    def get_lower_folder(self):
        self.lower_folder = self.get_path()
        self.update_user_info()

    def update_user_info(self):
        self.ui.l_user_info.setText("ID:%s\t姓名:%s\n上肢文件夹:%s\n下肢文件夹：%s"
                                    % (self.user_info[0], self.user_info[1], self.upper_folder, self.lower_folder))

    def save(self):
        motion = ["", "", ""]
        for j in range(0, 14):
            for i in range(0, 3):
                temp = self.ui.t_file_cfg.item(j, i).text()
                motion[i] = temp
            header = self.ui.t_file_cfg.verticalHeaderItem(j).text()
            file_cfg = [user_id, header] + motion

            sql = """INSERT INTO t_file_cfg (user_id, motion, active, mvc, passive) 
            VALUES (%s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, file_cfg)
        self.conn.commit()


if __name__ == '__main__':
    user_id = 1
    app = QApplication([])
    new_test = NewTest(1)
    new_test.ui.show()
    new_test.ui.exec_()
