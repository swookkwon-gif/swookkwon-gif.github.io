import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

years = np.arange(1999, 2010)
cage_films = [2, 2, 2, 3, 1, 1, 2, 3, 4, 1, 4]
drownings = [109, 102, 102, 98, 85, 95, 96, 98, 123, 94, 102]

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#FF9999'
ax1.set_xlabel('Year')
ax1.set_ylabel('Swimming Pool Drownings', color=color1)
ax1.plot(years, drownings, color=color1, marker='o', linewidth=3, label='Drownings')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(years)
ax1.set_ylim(80, 130)

ax2 = ax1.twinx()  
color2 = '#99CCFF'
ax2.set_ylabel('Nicolas Cage Films', color=color2)  
ax2.plot(years, cage_films, color=color2, marker='s', linewidth=3, linestyle='--', label='Nicolas Cage Films')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 6)

fig.suptitle('Spurious Correlation: Nicolas Cage vs. Pool Drownings\n(Data from Tyler Vigen)', fontsize=16)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_cage_real.png')
print("Graph saved")
