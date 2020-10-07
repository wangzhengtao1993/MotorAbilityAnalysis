# author:wzt

import xlrd
import pymysql

# Open the workbook and define the worksheet
book = xlrd.open_workbook("0922gxw_2020_09_22_192035_002_Odau_1主动屈髋.xlsx")
sheet = book.sheet_by_name("RMS")

# 建立一个MySQL连接
conn = pymysql.connect(host='localhost', user='root', password='123456', db='motor_ability_analysis',
                       port=3306)  # 打开数据库连接
cursor = conn.cursor()  # 执行数据库的操作是由cursor完成的,使用cursor()方法获取操作游标
# sql = "select * from t_rms_lower"  # 编写sql 查询语句,对应我的表名

query = """INSERT INTO t_rms_lower (test_id,time,rms_1,rms_2,rms_3,rms_4,rms_5,rms_6) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

for r in range(1, sheet.nrows):
    test_id = sheet.cell(r, 0).value
    time = sheet.cell(r, 1).value
    rms_1 = sheet.cell(r, 2).value
    rms_2 = sheet.cell(r, 3).value
    rms_3 = sheet.cell(r, 4).value
    rms_4 = sheet.cell(r, 5).value
    rms_5 = sheet.cell(r, 6).value
    rms_6 = sheet.cell(r, 7).value
    values = (test_id, time, rms_1, rms_2, rms_3, rms_4, rms_5, rms_6)
    # 执行sql语句
    cursor.execute(query, values)

cursor.close()  # 关闭游标
conn.commit()
conn.close()  # 关闭数据库连接
#
# # 打印结果
# print ""
# print "Done! "
# print ""
# columns = str(sheet.ncols)
# rows = str(sheet.nrows)
# print "我刚导入了 " %2B columns %2B " 列 and " %2B rows %2B " 行数据到MySQL!"


# import pymysql
# import xlwt
#
#
# def sql(sql):  # 定义一个执行SQL的函数
#     conn = pymysql.connect(host='localhost', user='root', password='123456', db='motor_ability_analysis', port=3306)  # 打开数据库连接
#     cursor = conn.cursor()  # 执行数据库的操作是由cursor完成的,使用cursor()方法获取操作游标
#     sql = "select * from t_rms_lower"  # 编写sql 查询语句,对应我的表名
#     cursor.execute(sql)  # 执行sql语句
#     # fields = cursor.description      #获取MYSQL里的数据字段
#     # cursor.scroll(0,mode='absolute') #重置游标位置(在同一个程序中执行二次操作用)
#     results = cursor.fetchall()  # 获取查询的所有记录
#     cursor.close()  # 关闭游标
#     conn.close()  # 关闭数据库连接
#     return results
#
#
# def wite_to_excel(name):
#     filename = name + '.xls'  # 定义Excel名字
#     wbk = xlwt.Workbook()  # 实例化一个Excel
#     sheet1 = wbk.add_sheet('文件名称', cell_overwrite_ok=True)  # 添加该Excel的第一个sheet，如有需要可依次添加sheet2等
#     fileds = ['名称', '邮箱']  # 直接定义结果集的各字段名
#
#     results = sql('select name,email from 表名')  # 调用函数执行SQL，获取结果集
#     print(results)
#
#     # for i in range(0, len(fileds)):  # EXCEL新表的第一行  写入字段信息
#     #     sheet1.write(0, i, fileds[i])
#     #
#     # # 执行数据插入
#     # for row in range(1, len(results) + 1):  # 第0行是字段名，从第一行开始插入数据
#     #     for col in range(0, len(fileds)):  # 依据字段个数进行列的插入
#     #         sheet1.write(row, col, results[row - 1][col])  # 第row行，第col列，插入数据（第1行，第i列，插入results[0][i]）
#     #
#     # # 执行保存
#     wbk.save(filename)
#
#
# wite_to_excel('文件名称')
