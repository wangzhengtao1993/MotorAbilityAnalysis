# author:wzt
import win32com.client as win32

from numpy import *
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
print(sheet.title)
sheet.title = "wzt"
wb.create_sheet(title="RMS")
print(wb.sheetnames)
wb.save("wzt.xlsx")


