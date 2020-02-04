import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM/gviz/tq?tqx=out:csv'
df = pd.read_csv(url)

df = df.rename(columns={'Province/State': 'Province', 'Country/Region': 'Country', 'Last Update': 'LastUpdate'})

df['Confirmed'] = df['Confirmed'].fillna(0)
df['Deaths'] = df['Deaths'].fillna(0)
df['Recovered'] = df['Recovered'].fillna(0)
df = df.astype({'Confirmed': 'int', 'Deaths': 'int', 'Recovered': 'int'})
df.to_csv('data.csv', index=False)
