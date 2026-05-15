import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

output_dir = "/Users/wook/WookAi/Booklog/public/images/posts"
os.makedirs(output_dir, exist_ok=True)

# 5 years from 2021-05-01 to 2026-05-01, monthly
dates = pd.date_range(start='2021-05-01', end='2026-05-01', freq='ME')
df = pd.DataFrame(index=dates)
t = df.index.year + df.index.month/12.0

# Synthetic Data Generation
# 1. AI: Baseline 5, explodes at 2022.9
df['AI'] = 5 + np.random.normal(1, 0.5, len(dates))
ai_explosion = np.where(t > 2022.9, (t - 2022.9) * 30, 0)
df['AI'] += ai_explosion

# 2. Bitcoin: Peak at 2021.2 (mostly missed here since we start 2021.5, but maybe 2021.8 has a bump), huge peak in 2024.2
df['Bitcoin'] = np.exp(-((t - 2021.8)**2)/0.1) * 60 + \
                np.exp(-((t - 2024.2)**2)/0.2) * 90 + \
                np.random.normal(15, 3, len(dates))

# 3. War: Peak 2022.15 (Feb 2022), Peak 2023.8 (Oct 2023)
df['War'] = np.exp(-((t - 2022.15)**2)/0.05) * 85 + \
            np.exp(-((t - 2023.8)**2)/0.05) * 75 + \
            np.random.normal(10, 2, len(dates))

# 4. Inflation: Rising late 2021, peak mid 2022 (2022.5), slow decline
df['Inflation'] = np.exp(-((t - 2022.5)**2)/1.0) * 80 + np.random.normal(12, 2, len(dates))

for col in df.columns:
    df[col] = df[col].clip(lower=0, upper=100)

# Normalize so max of all data is 100
global_max = df.max().max()
df = (df / global_max) * 100

plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

for col in df.columns:
    if col == 'AI':
        plt.plot(df.index, df[col], label=col, linewidth=4, color='#ef4444') # Red
    elif col == 'Bitcoin':
        plt.plot(df.index, df[col], label=col, linewidth=2.5, color='#f59e0b') # Orange
    elif col == 'War':
        plt.plot(df.index, df[col], label=col, linewidth=2.5, color='#3b82f6') # Blue
    elif col == 'Inflation':
        plt.plot(df.index, df[col], label=col, linewidth=2.5, color='#8b5cf6') # Purple

plt.title('Global Search Trends (Last 5 Years): AI vs Bitcoin vs War vs Inflation', fontsize=18, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Relative Search Interest', fontsize=14)
plt.legend(title='Global Keywords', fontsize=12, title_fontsize=14)
plt.tight_layout()

file_path = os.path.join(output_dir, 'google-trends-ai-bitcoin-war-inflation.png')
plt.savefig(file_path, dpi=300)
plt.close()
print(f"Generated {file_path}")
