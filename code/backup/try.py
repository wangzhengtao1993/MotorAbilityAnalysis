# # author:wzt
# path = r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\1.xlsx"
# path1 = path+ "x"
# print(path1)
import pandas as pd
import xlwings as xw
import xlwt
import xlrd
import os
#
#
data = pd.read_excel(r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\Process\1.xlsx", header=4)
print(data.columns)
print("新建肌电信号列")
for i in range(1,7):
    EMG = ("EMG_"+str(i))
    data[EMG] = None
print("新建RMS列")
for i in range(1,7):
    RMS = ("RMS_"+str(i))
    data[RMS] = None
data = data.set_index("Frame")
data.to_excel(r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\Process\1.xlsx")


# data["H"] = data["Analog_1"]/500
#
# # wb = xw.Book(r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\Process\0921wrj_2020_09_21_140406_001_Odau_1.xlsx")
# # sht = wb.sheets.add("new")
# # # data.values()
# # data.to_excel(r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\Process\0921wrj_2020_09_21_140406_001_Odau_1.xlsx",sheet_name="new")
# # # sht.range().value = data.values
# # # data.to_excel(excel_writer=writer, sheet_name="a")
# # wb.save()
# # wb.close()
# #
# # # s1 = pd.Series()
# # # s1.
# # print(data)
# #
# #
#
# #
# # d = {"x":100,
# #      "y":200,
# #      "z":300}
# # s1 = pd.Series(d)
# # print(s1.index)
# #
# #
# # L1 = [1,2,3]
# # L2 = ['x','y','z']
#
# s1 = pd.Series([1,2,3], index=[1,2,3],name="A")
# s2 = pd.Series([10,20,30], index=[1,2,3],name="B")
# df = pd.DataFrame({s1.name: s1,
#                    s2.name: s2})
# print(df)



