import pandas as pd

data = pd.read_csv('STRIKE_REPORTS (Public)_STRIKE_REPORTS.csv', sep=',', dtype=str)

data.head(5)
