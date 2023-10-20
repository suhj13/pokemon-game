import pandas as pd

df1 = pd.read_excel('database.xlsx', 'typeAdvantages')
# The variable columns gives the header of each column which is excluded in the 2D-array stored in version
columns = list(df1)
version = df1.values

index1 = 0
index2 = 0 
index3 = 0
for i in range(len(version)):
    if "Fire" == version[i][0]:
        break
    index1 += 1

for j in range(len(columns)):
    if "Fire" == columns[j]:
        break
    index2 += 1

for k in range(len(columns)):
    if "Flying" == columns[k]:
        break
    index3 += 1

multiplier1 = version[index1][index2]
multiplier2 = version[index1][index3]

print(columns)