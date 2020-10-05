# author:wzt
# import pymysql
from pymysql import *


class JD(object):
    def __init__(self):
        # 创建链接
        self.conn = connect(host='localhost', port=3306, user='root', password='123456', database='jingdong',
                            charset='utf8')
        # 获得cursor对象
        self.cursor = self.conn.cursor()
        print("connected")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        print("disconnected")

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

    @staticmethod
    def print_menu():
        print("________jingdong__________")
        print("1.所有商品")
        print("2.所有商品分类")
        print("3.所有商品品牌分类")
        print("4.添加品牌")
        print("5.根据名字查询商品")
        return input("请输入功能对应的序号:")

    def run(self):
        while True:
            num = self.print_menu()
            if num == "1":
                # 查询所有商品
                self.show_all_items()
            elif num == "2":
                # 查询分类
                self.show_cates()
            elif num == "3":
                # 显示品牌
                self.show_brands()
            elif num == "4":
                # 增加品牌
                self.add_brand()
            elif num == "5":
                # 增加品牌
                self.get_info_by_name()
            else:
                print("wrong input")


def main():
    # 1.创建京东对象
    jd = JD()
    # 2.调用这个对象的run方法，让其运行
    jd.run()


if __name__ == '__main__':
    main()
