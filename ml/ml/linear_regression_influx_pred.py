import re
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from util.common import load_from_mongo


def parse_number(str: str):
    str = str.replace(".", "")
    str = re.sub(r"\(.*\)", "", str)
    str = re.sub(r"\[.*\]", "", str)

    m = re.search("([0-9,]+)", str)
    if m is None:
        return int(str)

    num = m.group(0).replace(",", "")

    num = int(num)
    if re.search("thousand", str, re.IGNORECASE):
        num *= 1000

    if re.search("million", str, re.IGNORECASE):
        num *= 1000000

    return num


musuems = load_from_mongo()
musuems = [x for x in musuems if 'population' in x]
musuems = [x for x in musuems if 'Visitors' in x]
print(musuems)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10000)

df = pd.DataFrame(musuems)

df['Visitors'] = df['Visitors'].apply(lambda x: parse_number(x))
print(df.iloc[25])

# print(df['Public transit access count'].mean())
# pta_mean = df['Public transit access count'].mean()
# cs_mean = df['Public transit access count'].mean()
# df['Public transit access count'] = df['Public transit access count'].fillna(pta_mean)
# df['Collection size parsed'] = df['Collection size parsed'].fillna(cs_mean)
# print(df['population'])
# print(df['Public transit access count'])
# print(df['Collection size parsed'])
df['population'] = df['population'].apply(lambda x: int(x))
df = df[df['population'] > 0]

X = df['Visitors'].to_numpy().astype(int)
y = df['population'].to_numpy().astype(int)

# print(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
print(X_train.reshape(-1, 1), X_test.reshape(-1, 1), y_train, y_test)
reg = LinearRegression().fit(X_train.reshape(-1, 1), y_train)

preds = reg.predict(X_test.reshape(-1, 1))
print(preds, y_test)
# df[['Collection size', 'Public transit access count', 'Collection size parsed']]
