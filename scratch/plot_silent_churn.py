import matplotlib.pyplot as plt

plt.xkcd()
fig, ax = plt.subplots(figsize=(10, 4), dpi=120)

categories = ['Churned Customers']
vocal = [5]
silent = [95]

# Stacked bar chart
ax.barh(categories, silent, color='#34495E', label='Silent Churners (95%) - Leave without a word', height=0.5)
ax.barh(categories, vocal, left=silent, color='#E74C3C', label='Vocal Complainers (5%) - File CS tickets', height=0.5)

ax.set_xlim(0, 100)
ax.set_xlabel('Percentage of Lost Customers (%)', fontsize=14)
ax.set_title('The Iceberg of Customer Churn (Selection Bias)', fontsize=18, pad=20)

ax.annotate('We only analyze these 5%\nto "fix" the product!', xy=(97.5, 0.25), xytext=(60, 0.5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12, color='red')

ax.annotate('The massive unseen reality\n(They hated something else)', xy=(40, -0.2), xytext=(20, -0.4),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8), fontsize=12)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_yaxis().set_ticks([])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=1)

plt.tight_layout()
plt.savefig('/Users/wook/WookAi/Booklog/static/images/silent_churn_selection_bias.png', bbox_inches='tight', facecolor='white')
print("Saved silent_churn_selection_bias.png")
