import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

quarters = ['2022 Q1', 'Q2', 'Q3', 'Q4', '2023 Q1', 'Q2', 'Q3', 'Q4']
# US Retail Sales (approx. in Billions USD) - Shows Q4 Holiday Spikes
retail_sales = [1600, 1750, 1760, 1850, 1650, 1780, 1800, 1880]
# US Digital & Traditional Ad Spend (approx. in Billions USD) - Shows Q4 Spikes
ad_spend = [65, 70, 72, 85, 68, 72, 74, 90]

x = np.arange(len(quarters))

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#FF6666'
ax1.set_xlabel('Quarter', fontsize=12)
ax1.set_ylabel('US Total Ad Spend ($ Billions)', color=color1, fontsize=12)
ax1.plot(x, ad_spend, color=color1, marker='o', linewidth=3, label='Ad Spend (Billions)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(x)
ax1.set_xticklabels(quarters)
ax1.set_ylim(50, 100)

ax2 = ax1.twinx()  
color2 = '#3399FF'
ax2.set_ylabel('US Retail Sales ($ Billions)', color=color2, fontsize=12)  
ax2.plot(x, retail_sales, color=color2, marker='s', linewidth=3, linestyle='--', label='Retail Sales (Billions)')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(1500, 2000)

fig.suptitle('Macro Spurious Correlation:\nUS Ad Spend vs. Retail Sales (Q4 Seasonality)', fontsize=14)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

# Highlight Q4 Spikes
ax1.axvspan(2.5, 3.5, color='gray', alpha=0.1)
ax1.axvspan(6.5, 7.5, color='gray', alpha=0.1)
ax1.text(3, 95, 'Holiday\nSeason (Q4)', horizontalalignment='center', fontsize=10, color='gray')
ax1.text(7, 95, 'Holiday\nSeason (Q4)', horizontalalignment='center', fontsize=10, color='gray')

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_macro.png')
print("Graph saved")
