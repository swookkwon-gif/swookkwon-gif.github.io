import matplotlib.pyplot as plt
import numpy as np

# Apply xkcd style for sketch look
plt.xkcd()

fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

years = np.array([0, 3, 5, 10, 15])
# Based on historical SPIVA scorecards, over 15 years, ~60% of domestic equity funds merge or liquidate.
surviving_funds = np.array([100, 85, 75, 55, 42]) 
liquidated_funds = 100 - surviving_funds

ax.plot(years, surviving_funds, color='#2ECC71', linewidth=4, marker='o', markersize=8, label="Surviving Funds ('Winners')")
ax.plot(years, liquidated_funds, color='#E74C3C', linewidth=4, marker='X', markersize=8, linestyle='--', label="Merged/Liquidated ('Crashed Planes')")

ax.fill_between(years, 0, surviving_funds, color='#2ECC71', alpha=0.1)
ax.fill_between(years, 0, liquidated_funds, color='#E74C3C', alpha=0.1)

ax.set_title("The Mutual Fund Graveyard (15-Year Horizon)", fontsize=18, pad=20)
ax.set_xlabel("Years", fontsize=14)
ax.set_ylabel("Percentage of Funds (%)", fontsize=14)
ax.set_ylim(0, 105)
ax.set_xticks(years)

# Adding annotations
ax.annotate('Only ~42% survive.\nThe rest disappear from the data!', xy=(15, 42), xytext=(7, 20),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12)

ax.annotate('Start with 100% of funds', xy=(0, 100), xytext=(1, 80),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc="center left")

plt.tight_layout()
plt.savefig('/Users/wook/WookAi/Booklog/static/images/spiva_survivorship_bias.png', bbox_inches='tight', facecolor='white')
print("Saved spiva_survivorship_bias.png")
