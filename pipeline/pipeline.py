import sys
import pandas as pd

print(f"Parameters passed: {sys.argv}")
month = int(sys.argv[1])
print(f"Month: {month}")

df = pd.DataFrame({'day':[1,2,3],'num_passengers':[10,20,30]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet")

print("Pipeline successful")