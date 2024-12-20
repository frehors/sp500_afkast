import matplotlib.pyplot as plt
import pandas as pd

str_csv_path = r"C:\Users\frede\Downloads\chart.csv"
df = pd.read_csv(str_csv_path)
df["Return"] = df["Return"].div(100).add(1)

N = 100
years = 10

df_returns = pd.DataFrame()

for i in range(N):
    df_returns[f"{i}"] = df["Return"].reset_index(drop=True).sample(n=years, replace=True).reset_index(drop=True)


df_returns.cumprod().plot()
plt.show()

print("Average yearly return:", ((df_returns.cumprod().iloc[-1].mean() - 1) * 100*(1/years)).round(2), "%")
print("Median yearly return:", ((df_returns.cumprod().iloc[-1].median() - 1) * 100*(1/years)).round(2), "%")
#((
df_returns.cumprod().iloc[-1].subtract(1).mul(100).mul(1/years).round(2).hist(bins=30)

plt.show()




