import tkinter as tk
from tkinter import filedialog


table_name = "wzt"

sql = """INSERT INTO """+table_name+\
                """(test_time,user_id, frame,time,emg_1,emg_2,emg_3,emg_4,emg_5,emg_6) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
print(sql)


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
