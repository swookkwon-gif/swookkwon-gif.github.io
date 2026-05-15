import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

months = np.arange(1, 13)
# 2022 US Ice Cream Production (Approximate based on USDA 920M gallons total)
ice_cream = [60, 65, 75, 80, 85, 90, 95, 90, 80, 70, 65, 65]
# 2022 US Unintentional Drownings (Approximate based on CDC 4,509 total)
drownings = [200, 200, 250, 300, 450, 650, 750, 650, 400, 250, 200, 209]

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#FF6666'
ax1.set_xlabel('Month (2022)')
ax1.set_ylabel('US Ice Cream Production\n(Million Gallons)', color=color1)
ax1.plot(months, ice_cream, color=color1, marker='o', linewidth=3, label='Ice Cream Production')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(months)
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax1.set_ylim(40, 110)

ax2 = ax1.twinx()  
color2 = '#66B2FF'
ax2.set_ylabel('US Drowning Deaths', color=color2)  
ax2.plot(months, drownings, color=color2, marker='s', linewidth=3, linestyle='--', label='Drowning Deaths')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 900)

fig.suptitle('Spurious Correlation (Confounding Variable):\nIce Cream Production vs. Drowning Deaths (US, 2022)', fontsize=14)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_ice_cream.png')
print("Graph saved")
