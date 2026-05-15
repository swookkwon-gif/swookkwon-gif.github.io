import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

# Generate seasonal data (12 months)
months = np.arange(1, 13)
# Base temperature curve (peaks in July/August)
temp = 10 + 20 * np.sin(np.pi * (months - 4) / 6)
temp = np.clip(temp, 0, 35)

# Ice cream sales (highly correlated with temp)
ice_cream = 100 + 50 * temp + np.random.normal(0, 100, 12)
ice_cream = np.clip(ice_cream, 100, 2000)

# Drowning incidents (correlated with temp because more people swim)
drowning = 5 + 2 * temp + np.random.normal(0, 5, 12)
drowning = np.clip(drowning, 0, 100)

# Shark attacks (correlated with temp because more people in ocean)
shark_attacks = 1 + 0.5 * temp + np.random.normal(0, 2, 12)
shark_attacks = np.clip(shark_attacks, 0, 30)

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#FF9999'
ax1.set_xlabel('Month')
ax1.set_ylabel('Ice Cream Sales (Units)', color=color1)
ax1.plot(months, ice_cream, color=color1, marker='o', linewidth=3, label='Ice Cream Sales')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(months)
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

ax2 = ax1.twinx()  
color2 = '#99CCFF'
ax2.set_ylabel('Incidents (Drowning / Shark Attacks)', color=color2)  
ax2.plot(months, drowning, color=color2, marker='s', linewidth=3, linestyle='--', label='Drowning Incidents')

color3 = '#99FF99'
ax2.plot(months, shark_attacks, color=color3, marker='^', linewidth=3, linestyle=':', label='Shark Attacks')
ax2.tick_params(axis='y', labelcolor=color2)

fig.suptitle('Spurious Correlation:\nIce Cream vs. Drownings vs. Shark Attacks', fontsize=16)

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_ice_cream.png')
print("Graph saved to public/images/spurious_correlation_ice_cream.png")
