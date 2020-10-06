# author:wzt
import pandas as pd

# books = pd.read_excel("test1.xlsx",skiprows=9, usecols="D:E",dtype={"ID":str})
# print(books)
# for i in books.index:
#     books["ID"].at[i] = i+1
#
# print(books)


f = "0921wrj_2020_09_21_140406_001_Odau_1"

print(f[26:29])
file_name = pd.read_excel("邬如靖.xlsx", dtype=str)
print(file_name.columns[2])
print(file_name)

print(file_name.iloc[1, 3])

src_file_name = f[26:29]

src_file_name_list = []
for motion in range(0, 6):
    for motion_pattern in range(2, 5):
        src_file_name = f[0:26]+file_name.iloc[motion,motion_pattern]+"_Odau_1.xlsx"
        src_file_name_list.append(src_file_name)
        new_file_name = f[0:26] + file_name.iloc[motion, motion_pattern] + "_Odau_1" + \
                                file_name.columns[motion_pattern] + file_name.iloc[motion, 1] + ".xlsx"
        print(new_file_name)
print(src_file_name_list)

#
# for motion in range(1, 7):
#     for type in range(2, 5):
#         new_file_name = f+file_name.columns[type]+file_name.iloc[motion,1]
#
# print(new_file_name)