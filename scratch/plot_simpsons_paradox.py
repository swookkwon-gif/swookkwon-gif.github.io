import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

# Generate data for Group 1
x1 = np.random.normal(3, 1, 50)
y1 = -0.8 * x1 + 8 + np.random.normal(0, 0.5, 50)

# Generate data for Group 2
x2 = np.random.normal(6, 1, 50)
y2 = -0.8 * x2 + 13 + np.random.normal(0, 0.5, 50)

# Generate data for Group 3
x3 = np.random.normal(9, 1, 50)
y3 = -0.8 * x3 + 18 + np.random.normal(0, 0.5, 50)

x = np.concatenate([x1, x2, x3])
y = np.concatenate([y1, y2, y3])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: The Aggregate (Misleading Trend)
ax1.scatter(x, y, color='gray', alpha=0.7)
m, b = np.polyfit(x, y, 1)
ax1.plot(x, m*x + b, color='black', linestyle='--', linewidth=2, label=f'Overall Trend (Positive)')
ax1.set_title("1. The Illusion (Overall Data)")
ax1.legend()
ax1.set_xticks([])
ax1.set_yticks([])

# Plot 2: The Truth (Segmented Data)
ax2.scatter(x1, y1, color='#FF9999', label='Group A')
m1, b1 = np.polyfit(x1, y1, 1)
ax2.plot(x1, m1*x1 + b1, color='red', linewidth=2)

ax2.scatter(x2, y2, color='#99CCFF', label='Group B')
m2, b2 = np.polyfit(x2, y2, 1)
ax2.plot(x2, m2*x2 + b2, color='blue', linewidth=2)

ax2.scatter(x3, y3, color='#99FF99', label='Group C')
m3, b3 = np.polyfit(x3, y3, 1)
ax2.plot(x3, m3*x3 + b3, color='green', linewidth=2)

ax2.set_title("2. The Reality (Segmented Data)")
ax2.legend()
ax2.set_xticks([])
ax2.set_yticks([])

plt.tight_layout()
plt.savefig('/Users/wook/.gemini/antigravity/brain/42eeee43-60c7-4ddf-b76e-da2409f512ec/simpsons_paradox_graph.png')
print("Graph saved")
