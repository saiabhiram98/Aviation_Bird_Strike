import pandas as pd

df = pd.read_csv("STRIKE_REPORTS.csv", sep = ',', dtype = str)

print(df.head(5))

for i in df:
    print(i)
    if i[3]    == False:
        print("FALSE")