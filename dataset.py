from AutoClean import AutoClean
import pandas as pd 

df = pd.read_csv('messy_data.csv')
pipeline = AutoClean(df)
print(pipeline.output)
