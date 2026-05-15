import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq

output_dir = "/Users/wook/WookAi/Booklog/public/images/posts"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

pytrend = TrendReq(hl='en-US', tz=360)

kws = ['AI', 'Bitcoin', 'War', 'Inflation']
print(f"Fetching {kws}...")

pytrend.build_payload(kws, timeframe='today 5-y')
df = pytrend.interest_over_time()

if not df.empty and 'isPartial' in df.columns:
    df = df.drop(columns=['isPartial'])

df_monthly = df.resample('ME').mean()

plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'AppleGothic'

for col in kws:
    linewidth = 4 if col == 'AI' else 2
    color = 'red' if col == 'AI' else None
    if color:
        plt.plot(df_monthly.index, df_monthly[col], label=col, linewidth=linewidth, color=color)
    else:
        plt.plot(df_monthly.index, df_monthly[col], label=col, linewidth=linewidth)

plt.title('Global Search Trends (Last 5 Years): AI vs Bitcoin vs War vs Inflation', fontsize=18, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Relative Search Interest')
plt.legend(title='Keywords')
plt.tight_layout()

file_path = os.path.join(output_dir, 'google-trends-ai-bitcoin-war-inflation.png')
plt.savefig(file_path, dpi=300)
plt.close()
print(f"Generated {file_path}")
