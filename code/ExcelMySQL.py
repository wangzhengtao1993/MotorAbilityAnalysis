# author:wzt
# import pymysql
from pymysql import *


class ExcelMySQL(object):

    def __init__(self,folder):
        # 创建链接
        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis',
                            charset='utf8')
        # 获得cursor对象
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print("database motor_ability_analysis")

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        for temp in self.cursor.fetchall():
            print(temp)

    def show_all_items(self):
        sql = "select * from goods;"
        self.execute_sql(sql)

    def show_cates(self):
        sql = "select name from goods_cates;"
        self.execute_sql(sql)

    def show_brands(self):
        sql = "select name from goods_brands;"
        self.execute_sql(sql)

    def add_brand(self):
        brand_name = input("输入新品牌名称：")
        sql = "insert into goods_brands (name) values('%s');" % brand_name
        self.cursor.execute(sql)
        self.conn.commit()

    def add_item(self):
        brand_name = input("输入新产品名称：")
        sql = "insert into goods_brands (name) values('%s');" % brand_name
        # commit后才能保存
        self.conn.commit()

    def get_info_by_name(self):
        find_name = input("请输入要查询的商品名字：")
        sql = """select * from goods where name=%s"""

        print("--->%s<---" % sql)
        self.cursor.execute(sql, [find_name])
        print(self.cursor.fetchall())



    def run(self):




def main():
    # 1.指定文件夹
    folder = r"D:\code\运动能力分析实验\0924wj_2020_09_24_200721"

    em = ExcelMySQL(folder)
    # 2.调用这个对象的run方法，让其运行
    em.run()


if __name__ == '__main__':
    main()
