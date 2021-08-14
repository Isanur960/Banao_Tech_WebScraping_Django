import pandas as pd
import os

base = os.getcwd()
filename = os.path.join(base, 'data.xlsx')
data = pd.read_excel(filename)
dh = data.head()
interest_list = pd.DataFrame(data, columns=['Interested_Group'])
for row in interest_list.values:
    print(type(row[0]))
