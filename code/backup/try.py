import tkinter as tk
from tkinter import filedialog





# from pymysql import *
# import pymysql
# from numpy import *
#
#
# def slid_window(raw):
#     # 一次传入re_raw的一列
#     length = len(raw)
#     step = self.win_set[0]
#     width = self.win_set[1]
#     frame = int((length - width) / step + 1)  # 处理后的帧数
#     sw = zeros((frame, width), dtype=float)  # 初始化矩阵，每行是一个时间窗
#     i = 0
#     while i < length - width + 1:
#         # 每行新建空数组，作为window
#         window = array([])
#         for j in range(0, width):
#             # 每列从i添加到i+width
#             window = append(window, raw[i + j])
#         # 生成sw矩阵
#         sw[int(i / step)] = window
#         i += step
#     return sw
#
#
# if __name__ == '__main__':
#     conn = connect(host='localhost', port=3306, user='root', password='123456',
#                    database='motor_ability_analysis', charset='utf8')
#     cursor = conn.cursor()
#     print("database motor_ability_analysis connected")
#     sql = "select emg_1 from t_emg_mvc_ankle_extension "
#     print("sql:", sql)
#     cursor.execute(sql)
#
#     raw_emg = cursor.fetchall()
#     frames_num = len(raw_emg)
#     emg = zeros(frames_num, dtype=float)
#     for i in range(frames_num):
#         emg[i] = raw_emg[i][0]
#
#     print(emg)
#     print(frames_num)
#     print(raw_emg[0][0] * 100)

# data = []
# for temp in raw_emg:
#     print(temp[0])
#     data.append(temp[0])
# print(data)
# #
# # def output(array):
# #     for i in range(len(array)):
# #         for j in range(len(array[0])):
# #             print(array[i][j],end='')
# #             print('   ',end='')
# #         print(' ')
# def output(array):
#     for i in range(len(array)):
#         for j in range(len(array[0])):
#             print(array[i][j], end='')
#             print('   ', end='')
#         print(' ')
#
#
# print(output(raw_emg))

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
