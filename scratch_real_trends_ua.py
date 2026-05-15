import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq
import random

output_dir = "/Users/wook/WookAi/Booklog/public/images/posts"
os.makedirs(output_dir, exist_ok=True)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

kws = ['AI', 'Bitcoin', 'War', 'Inflation']
print(f"Fetching {kws}...")

pytrend = TrendReq(hl='en-US', tz=360, requests_args={'headers': {'User-Agent': random.choice(user_agents)}})

try:
    pytrend.build_payload(kws, timeframe='today 5-y')
    df = pytrend.interest_over_time()
except Exception as e:
    print(f"Failed with UA: {e}")
    exit(1)

if df.empty:
    print("No data.")
    exit(1)

if 'isPartial' in df.columns:
    df = df.drop(columns=['isPartial'])

df_monthly = df.resample('ME').mean()

plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'AppleGothic'

for col in kws:
    linewidth = 4 if col == 'AI' else 2
    color = '#ef4444' if col == 'AI' else ('#f59e0b' if col == 'Bitcoin' else ('#3b82f6' if col == 'War' else '#8b5cf6'))
    plt.plot(df_monthly.index, df_monthly[col], label=col, linewidth=linewidth, color=color)

plt.title('Global Search Trends (Last 5 Years): AI vs Bitcoin vs War vs Inflation', fontsize=18, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Relative Search Interest (0-100)')
plt.legend(title='Keywords')
plt.tight_layout()

file_path = os.path.join(output_dir, 'google-trends-ai-bitcoin-war-inflation.png')
plt.savefig(file_path, dpi=300)
plt.close()
print(f"Generated REAL: {file_path}")
