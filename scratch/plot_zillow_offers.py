import matplotlib.pyplot as plt
import numpy as np

# Apply xkcd style for sketch look
plt.xkcd()

fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

# Time points
months = np.arange(1, 25)
labels = [f"Month {m}" for m in months]

# Simulated Housing Price Reality (Stable -> Volatile/Dropping)
actual_price = 300 + 2 * months[:12] + np.random.normal(0, 5, 12)
actual_price = np.append(actual_price, 324 + np.cumsum(np.random.normal(-3, 8, 12)))

# Overfitted Algorithm Prediction (Trained on the stable past)
predicted_price = 300 + 2.5 * months 

# Plotting
ax.plot(months, predicted_price, color='#FF5733', linewidth=3, label="Zestimate AI Prediction (Overfitted)")
ax.plot(months, actual_price, color='#3388FF', linewidth=3, label="Actual Housing Market (Reality)")

# Highlight the divergence zone (Zillow buying aggressively)
ax.fill_between(months[12:], actual_price[12:], predicted_price[12:], color='red', alpha=0.1, label="$-500M Loss Zone (Bought high, Sold low)")

ax.set_title("Zillow Offers Algorithm Failure (Concept Drift)", fontsize=18, pad=20)
ax.set_xlabel("Time (Months)", fontsize=14)
ax.set_ylabel("Housing Price", fontsize=14)

# Adding annotations
ax.annotate('Pandemic Market Shift\n(Concept Drift Begins)', xy=(12.5, actual_price[12]), xytext=(7, 400),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=11)

ax.annotate('Algorithm kept predicting\nprices would go up forever', xy=(20, predicted_price[19]), xytext=(12, 360),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=11)

ax.annotate('iBuying Shutdown\n(25% Staff Laid Off)', xy=(23, actual_price[22]), xytext=(15, 250),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=11)


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc="upper left")

plt.tight_layout()
plt.savefig('/Users/wook/WookAi/Booklog/static/images/zillow_concept_drift.png', bbox_inches='tight', facecolor='white')
print("Saved zillow_concept_drift.png")
