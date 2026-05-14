import matplotlib.pyplot as plt
import numpy as np

plt.xkcd()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=120)

# Data
categories = ['Mobile', 'Desktop']
camp_a_rates = [10.0, 5.0]
camp_b_rates = [8.0, 4.0]

overall_categories = ['Overall Total']
camp_a_overall = [5.45]
camp_b_overall = [7.63]

x = np.arange(len(categories))
width = 0.35

# Subplot 1: Segmented
rects1_a = ax1.bar(x - width/2, camp_a_rates, width, label='Campaign A (Control)', color='#2980B9')
rects1_b = ax1.bar(x + width/2, camp_b_rates, width, label='Campaign B (Treatment)', color='#E74C3C')

ax1.set_ylabel('Conversion Rate (%)', fontsize=14)
ax1.set_title('Segmented by Device (Campaign A Wins Both!)', fontsize=16)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=14)
ax1.legend()

# Subplot 2: Overall
x_overall = np.arange(len(overall_categories))
rects2_a = ax2.bar(x_overall - width/2, camp_a_overall, width, label='Campaign A', color='#2980B9')
rects2_b = ax2.bar(x_overall + width/2, camp_b_overall, width, label='Campaign B', color='#E74C3C')

ax2.set_ylabel('Conversion Rate (%)', fontsize=14)
ax2.set_title('Overall Performance (Campaign B Wins?!)', fontsize=16)
ax2.set_xticks(x_overall)
ax2.set_xticklabels(overall_categories, fontsize=14)

ax2.annotate('Simpson\'s Paradox!', xy=(0.17, 7.63), xytext=(0.5, 9),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=14, color='red')

# Adding text labels on bars
def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)

autolabel(rects1_a, ax1)
autolabel(rects1_b, ax1)
autolabel(rects2_a, ax2)
autolabel(rects2_b, ax2)

ax1.set_ylim(0, 12)
ax2.set_ylim(0, 12)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/Users/wook/WookAi/Booklog/static/images/simpsons_paradox_ab_test.png', bbox_inches='tight', facecolor='white')
print("Saved simpsons_paradox_ab_test.png")
