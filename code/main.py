# author:wzt
import pandas as pd


# info = pd.read_excel("../Data/Info.xlsx")
# print(info.shape)
# print(info)
# print(info.columns)
# info = info.set_index("ID")
# info.to_excel("../Data/test.xlsx")
# print("Done!")


s1 = pd.Series([1,2,3], index=[1,2,3],name="A")
s2 = pd.Series([10,20,30], index=[1,2,3],name="B")

df = pd.DataFrame({s1.name: s1, s2.name: s2})
print(df)
