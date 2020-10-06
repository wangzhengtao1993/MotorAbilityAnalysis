# author:wzt
import pandas as pd

books = pd.read_excel("test1.xlsx",skiprows=9, usecols="D:E",dtype={"ID":str})
print(books)
for i in books.index:
    books["ID"].at[i] = i+1

print(books)

