# author:wzt
from PySide2.QtWidgets import QApplication, QMessageBox, QDialog
from PySide2.QtUiTools import QUiLoader
from pymysql import *


class OpenUser(object):
    """
    新建受试者信息并存入数据库
    """

    def __init__(self):
        # 链接数据库
        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis',
                            charset='utf8')
        # 获得cursor对象
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")
        # 调用ui文件
        self.ui = QUiLoader().load('ui_design/new_user.ui')  # 路径用/，以免被认成转义，与系统用法不冲突

        # 槽函数，点击按钮调用对应函数
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.cancel_btn.clicked.connect(self.cancel)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print("database motor_ability_analysis disconnected")

    def cancel(self):
        self.ui.close()

    def show_all(self):
        pass

    def open(self):
        # 获取QLineEDit文本框内容
        info = (self.ui.le_name.text(),
                self.ui.cb_gender.currentText(),
                self.ui.le_year_of_birth.text(),
                self.ui.cb_handedness.currentText(),
                self.ui.le_height.text(),
                self.ui.le_weight.text(),
                self.ui.le_waistline.text(),
                self.ui.le_upperarm.text(),
                self.ui.le_forearm.text(),
                self.ui.le_thigh.text(),
                self.ui.le_shank.text()
                )
        print(info)

        if len(info[2]) != 4:
            print(QMessageBox.about(self.ui, 'Warning', '生日仅能为4位年份'))
        else:
            for item in info:
                if not item:
                    print(QMessageBox.about(self.ui, 'Warning', '必要信息缺失'))
                    break

        # 保存至数据库
        sql = """INSERT INTO t_user (name, gender, year_of_birth, handedness, height, weight, waistline, 
        upperarm, forearm, thigh, shank) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, info)
        self.conn.commit()
        self.ui.close()


if __name__ == '__main__':
    app = QApplication([])
    new_user = NewUser()
    new_user.ui.show()
    new_user.ui.exec_()

