import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

fig, ax = plt.subplots(figsize=(8, 6))

categories = ['Observational Data\n(Spurious Correlation)', 'Controlled Experiment\n(True Causal Effect)']
roi_values = [1500, -63]
colors = ['#FF9999', '#99CCFF']

bars = ax.bar(categories, roi_values, color=colors, width=0.5)

ax.set_ylabel('Estimated Return on Investment (ROI) %', fontsize=12)
ax.set_title('eBay Paid Search Experiment (Blake, Nosko, Tadelis, 2015)\nSpurious Correlation vs. Causation', fontsize=14)

# Add text labels on top of bars
for bar, value in zip(bars, roi_values):
    yval = bar.get_height()
    if value > 0:
        ax.text(bar.get_x() + bar.get_width()/2, yval + 50, f'+{value}%', ha='center', va='bottom', fontsize=14, fontweight='bold')
    else:
        ax.text(bar.get_x() + bar.get_width()/2, yval - 150, f'{value}%', ha='center', va='top', fontsize=14, fontweight='bold')

ax.axhline(0, color='black', linewidth=1.5)

plt.tight_layout()
plt.savefig('public/images/spurious_correlation_ebay.png')
print("Graph saved")
