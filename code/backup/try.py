import tkinter as tk
from tkinter import filedialog

from pymysql import *

user_id = 4
conn = connect(host='localhost', port=3306, user='root',
               password='123456', database='motor_ability_analysis', charset='utf8')
cursor = conn.cursor()

motion_mode = "active"
motion_name = "屈肩"


sql = """SELECT %s FROM `t_file_cfg` WHERE (`user_id` = '%s' and motion = '%s') """ % (motion_mode, user_id, motion_name)



cursor.execute(sql)
t_file_cfg = cursor.fetchone()
print(t_file_cfg[0])

motion_name = {1: "上肢静息",
               2: "屈肩"}

print(motion_name[1])

# motion_name = {"上肢静息": 0,
#                "屈肩": 1,
#                "伸肩": 2,
#                "屈肘": 3,
#                "伸肘": 4,
#                "屈腕": 5,
#                "伸腕": 6,
#                }
#
# motion_mode = {"主动": 3,
#                "MVC": 4,
#                "被动": 5,
#                }
# print(motion_mode(1))
# file_id = t_file_cfg[motion_name["屈肩"]][motion_mode["MVC"]]
# print(file_id)


# def get_file_id(motion_name,motion_mode)

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
