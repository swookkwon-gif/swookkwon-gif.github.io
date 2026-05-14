import matplotlib.pyplot as plt
import numpy as np

plt.xkcd()
np.random.seed(42)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=120)

# Generate random points
x = np.random.uniform(0, 10, 50)
y = np.random.uniform(0, 10, 50)

# Panel 1: Random points
ax1.scatter(x, y, color='black', s=30)
ax1.set_title('1. Shoot Randomly\n(Collect Big Data)', fontsize=16, pad=15)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')

# Panel 2: Draw the bullseye around a cluster
ax2.scatter(x, y, color='black', s=30)
ax2.set_title('2. Draw the Target Later\n(Claim "I am a Sharpshooter!")', fontsize=16, pad=15)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')

# Find a dense cluster to draw the target
# Visually, there's a cluster around (1.5, 6) in this seed
target_x, target_y = 1.5, 6.0

# Draw target circles
circle1 = plt.Circle((target_x, target_y), 1.5, color='red', fill=False, linewidth=3)
circle2 = plt.Circle((target_x, target_y), 1.0, color='red', fill=False, linewidth=3)
circle3 = plt.Circle((target_x, target_y), 0.5, color='red', fill=True, alpha=0.5)

ax2.add_patch(circle1)
ax2.add_patch(circle2)
ax2.add_patch(circle3)

ax2.annotate('Look at my\nperfect accuracy!', xy=(target_x+1.5, target_y), xytext=(target_x+3, target_y-2),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=14)

plt.tight_layout()
plt.savefig('/Users/wook/WookAi/Booklog/static/images/texas_sharpshooter.png', bbox_inches='tight', facecolor='white')
print("Saved texas_sharpshooter.png")
