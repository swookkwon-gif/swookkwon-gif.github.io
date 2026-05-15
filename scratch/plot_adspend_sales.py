import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

months = np.arange(1, 13)
# Synthetic Marketing Data (Spurious Correlation due to Seasonality)
ad_spend = [10, 12, 15, 13, 16, 20, 18, 15, 25, 40, 80, 60]
sales = [100, 110, 120, 115, 125, 140, 135, 120, 160, 250, 600, 450]

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#FF9933'
ax1.set_xlabel('Month')
ax1.set_ylabel('Ad Spend ($k)', color=color1)
ax1.plot(months, ad_spend, color=color1, marker='o', linewidth=3, label='Ad Spend')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(months)
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax1.set_ylim(0, 100)

ax2 = ax1.twinx()  
color2 = '#3399FF'
ax2.set_ylabel('Sales ($k)', color=color2)  
ax2.plot(months, sales, color=color2, marker='s', linewidth=3, linestyle='--', label='Sales')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 800)

fig.suptitle('Business Trap:\nAd Spend vs. Sales (Seasonality as Confounding Variable)', fontsize=14)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

# Annotate Black Friday Season
ax1.axvspan(10.5, 12.5, color='gray', alpha=0.1)
ax1.text(11.5, 85, 'Holiday\nSeason', horizontalalignment='center', fontsize=12, color='gray')

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_ad_sales.png')
print("Graph saved")
