import tkinter as tk
from tkinter import filedialog

from pymysql import *
user_id = 4
conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis', charset='utf8')
cursor = conn.cursor()
sql = """SELECT * FROM `t_file_cfg` WHERE `user_id` = '%s'""" % user_id
cursor.execute(sql)
user_info = cursor.fetchall()
print(user_info)

# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askdirectory()
# import win32ui
#
# a = ["user_id", "motion", "active", "mvc", "passive"]
# b = ["active", "mvc", "passive"]
# c = a + b
# print(c)
#
# # dlg = win32ui.CreateFileDialog(1)
# dlg = win32ui.CreateFileDialog(1)
#
# # 默认目录
# # dlg.SetOFNInitialDir('C:/')
# # 显示对话框
# dlg.DoModal()
# # 获取用户选择的文件全路径
# filename = dlg.GetPathName()
#
# windows_path='C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Xmanager 5'
# linux_path=windows_path.replace('\\','/')
# print(windows_path)
# print(linux_path)
# path = linux_path.replace()
