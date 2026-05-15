import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

fig, ax = plt.subplots(figsize=(8, 6))

categories = ['Observational Data\n(Spurious Correlation)', 'Randomized Controlled Trial\n(True Causal Lift)']
# Using the "off by a factor of 3" finding
lift_values = [300, 100]
colors = ['#FF9999', '#99CCFF']

bars = ax.bar(categories, lift_values, color=colors, width=0.5)

ax.set_ylabel('Estimated Lift in Purchases (%)', fontsize=12)
ax.set_title('Facebook Ads Experiment (Gordon et al., 2019)\nTargeting Bias vs. True Lift', fontsize=14)

for bar, value in zip(bars, lift_values):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10, f'+{value}%', ha='center', va='bottom', fontsize=14, fontweight='bold')

ax.set_ylim(0, 350)
ax.axhline(0, color='black', linewidth=1.5)

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_facebook.png')
print("Graph saved")
