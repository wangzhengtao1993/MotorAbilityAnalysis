import win32com.client as win32

excel = win32.gencache.EnsureDispatch('Excel.Application')


# # # author:wzt
# # path = r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\1.xlsx"
# # path1 = path+ "x"
# # print(path1)
# import pandas as pd
# import xlwings as xw
# import xlwt
# import xlrd
# import os
# import win32com.client as win32
# excel = win32.gencache.EnsureDispatch('Excel.Application')
#
# #
# # writer = pd.ExcelWriter(r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\Process\0921wrj_2020_09_21_140406_001_Odau_1.xlsx")
# # data = pd.read_excel(r"D:\code\运动能力分析实验\0921wrj_2020_09_21_140406\Process\0921wrj_2020_09_21_140406_001_Odau_1.xlsx", header=4)
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



