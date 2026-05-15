import matplotlib.pyplot as plt
import os

with plt.xkcd():
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
    
    # Hide axes
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Left Side: CMO Dashboard
    ax.text(0.2, 0.8, 'CMO Dashboard', fontsize=22, ha='center', weight='bold')
    
    ax.text(0.2, 0.6, '"ROAS 300%!"', fontsize=18, ha='center')
    ax.text(0.2, 0.45, '"CTR 5%!"', fontsize=18, ha='center')
    ax.text(0.2, 0.3, '"Millions of Impressions!"', fontsize=16, ha='center')
    
    # Right Side: CEO Reality
    ax.text(0.8, 0.8, 'CEO Bank Account', fontsize=22, ha='center', weight='bold')
    
    ax.text(0.8, 0.6, '"Where is the cash?"', fontsize=18, ha='center')
    ax.text(0.8, 0.45, '"Growth is flat..."', fontsize=18, ha='center')
    ax.text(0.8, 0.3, '"Profits are down!"', fontsize=16, ha='center')
    
    # The gap/arrow
    ax.annotate('', xy=(0.35, 0.5), xytext=(0.65, 0.5),
                arrowprops=dict(arrowstyle='<|-|>', lw=2, color='black'))
    
    ax.text(0.5, 0.5, 'The Data\nDisconnect', fontsize=20, ha='center', va='center', rotation=0, 
            bbox=dict(boxstyle="circle,pad=0.5", fc="white", ec="black", lw=2, ls='--'))
    
    # Add a floor line
    ax.plot([0.1, 0.9], [0.1, 0.1], color='black', lw=3)
    
    plt.tight_layout()
    output_path = '/Users/wook/WookAi/Booklog/public/images/ceo_cmo_data_disconnect.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Generated sketchy diagram at {output_path}")

