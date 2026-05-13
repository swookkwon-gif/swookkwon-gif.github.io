import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

output_dir = "/Users/wook/WookAi/Booklog/public/images/posts"
csv_path = "/Users/wook/WookAi/Booklog/scratch/20yrs-5keywords.csv"

# Read the CSV
df = pd.read_csv(csv_path)

# Ensure columns are what we expect
df.columns = ['Date', 'AI', 'Bitcoin', 'War', 'iPhone', 'Financial Crisis']

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Drop Financial Crisis
df = df.drop(columns=['Financial Crisis'])

# Replace any '<1' with 0.5 and convert to numeric
for col in df.columns:
    if df[col].dtype == object:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('<1', '0.5'), errors='coerce')

plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# Plot all columns
colors = {
    'AI': '#ef4444',            # Red
    'Bitcoin': '#f59e0b',       # Orange
    'War': '#3b82f6',           # Blue
    'iPhone': '#10b981'         # Green
}

for col in df.columns:
    linewidth = 4 if col == 'AI' else 2
    color = colors.get(col, '#999999')
    plt.plot(df.index, df[col], label=col, linewidth=linewidth, color=color)

plt.title('20-Year Global Search Trends: AI vs Bitcoin vs War vs iPhone', fontsize=18, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Relative Search Interest (0-100)', fontsize=14)
plt.legend(title='Keywords', fontsize=12, title_fontsize=14)
plt.tight_layout()

file_path = os.path.join(output_dir, 'google-trends-mega-20yrs.png')
plt.savefig(file_path, dpi=300)
plt.close()
print(f"Generated REAL 20-year chart from user CSV: {file_path}")
