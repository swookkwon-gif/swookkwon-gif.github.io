import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq

output_dir = "/Users/wook/WookAi/Booklog/public/images/posts"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# Try pytrends with some backoff
success = False
df = pd.DataFrame()

kws = ['AI', 'Bitcoin', 'War', 'Inflation']
print(f"Fetching {kws}...")

for attempt in range(3):
    try:
        pytrend = TrendReq(hl='en-US', tz=360, retries=3, backoff_factor=1)
        pytrend.build_payload(kws, timeframe='today 5-y')
        df = pytrend.interest_over_time()
        success = True
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(5)

if not success or df.empty:
    print("Failed to fetch REAL data from Google Trends.")
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
print(f"Successfully generated REAL trends chart: {file_path}")
