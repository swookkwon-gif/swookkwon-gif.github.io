import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

output_dir = "/Users/wook/WookAi/Booklog/public/images/posts"
csv_path = "/Users/wook/WookAi/Booklog/scratch/multiTimeline.csv"

if not os.path.exists(csv_path):
    print(f"CSV not found at {csv_path}")
    exit(1)

# Google Trends CSV usually has 2-3 lines of header
# We skip the first 2 rows
df = pd.read_csv(csv_path, skiprows=2)
df.columns = ['Date', 'AI', 'Bitcoin', 'War', 'Inflation']

# Remove rows with text like 'Week' or incomplete data if necessary
# Convert strings to numeric
for col in ['AI', 'Bitcoin', 'War', 'Inflation']:
    df[col] = pd.to_numeric(df[col].replace('<1', '0.5'), errors='coerce')

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.dropna()

# Resample to monthly
df_monthly = df.resample('ME').mean()

plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

for col in df_monthly.columns:
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
print(f"Generated REAL chart from CSV: {file_path}")
