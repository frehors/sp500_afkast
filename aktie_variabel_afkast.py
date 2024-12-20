import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats.mstats import gmean

str_csv_path = r"C:\Users\frede\Downloads\chart.csv"
df = pd.read_csv(str_csv_path)
df["Return"] = df["Return"].div(100).add(1)

N = 10000
years = 10

dict_cols = {}
for i in range(N):
    dict_cols[i] = df["Return"].reset_index(drop=True).sample(n=years, replace=True).reset_index(drop=True)

df_returns = pd.DataFrame(dict_cols)

geometric_means = df_returns.apply(gmean, axis=0) - 1  # Subtract 1 to get growth rate
avg_return = (geometric_means.mean() * 100).round(2)
median_return = (geometric_means.median() * 100).round(2)


sharpe_ratios = df_returns.subtract(1).mean(axis=0) / df_returns.subtract(1).std(axis=0)
sharpe_ratios_mean = sharpe_ratios.mean().round(2)
sharpe_ratios_median = sharpe_ratios.median().round(2)
# Plot
fig, axes = plt.subplots(1, 3, figsize=(14, 6))

df_returns.cumprod().subtract(1).mul(100).plot(ax=axes[0], legend=False)
axes[0].set_xlabel("year")
axes[0].set_ylabel("cumulative return %")

df_returns.cumprod().iloc[-1].subtract(1).mul(100).round(2).hist(ax=axes[1], bins=30, density=True, alpha=0.6)
sns.kdeplot(df_returns.cumprod().iloc[-1].subtract(1).mul(100).round(2), ax=axes[1], color='red', lw=2)
axes[1].set_xlabel("yearly return (%)")
axes[1].set_ylabel("density")

(df_returns.subtract(1).mean(axis=0) / df_returns.subtract(1).std(axis=0)).hist(ax=axes[2], bins=30, density=True, alpha=0.6)
sns.kdeplot(df_returns.subtract(1).mean(axis=0) / df_returns.subtract(1).std(axis=0), ax=axes[2], color='red', lw=2)
axes[2].set_xlabel("sharpe ratio")
axes[2].set_ylabel("density")

textstr = (f"avg yearly return: {avg_return}%"
           f"\nmedian yearly return: {median_return}%"
           f"\navg sharpe : {sharpe_ratios_mean}"
           f"\nmedian sharpe: {sharpe_ratios_median}")
props = dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=1.5)
axes[2].text(1.05, 0.9, textstr, transform=axes[2].transAxes, fontsize=12,
             verticalalignment='top', horizontalalignment='left', bbox=props)

fig.suptitle(f"SP500 Simulated {years} year return, (N={N}, Years={df['Year'].min()} - {df['Year'].max()}), sample annual returns with replacmenet", fontsize=16)
plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.show()

