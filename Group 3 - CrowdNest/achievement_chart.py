import numpy as np
import matplotlib.pyplot as plt

# Achievement data
categories = [
    'User Mgmt', 
    'Donation Mgmt', 
    'Request Flow', 
    'DB Interact', 
    'Comm System', 
    'Security', 
    'UI/UX'
]
achievements = [100, 90, 90, 100, 95, 100, 95]

# Create the pie chart
plt.figure(figsize=(10, 8))

# Use a color palette
colors = plt.cm.Pastel1(np.linspace(0, 1, len(categories)))

# Create pie chart with percentage labels
plt.pie(
    achievements, 
    labels=[f'{cat}\n{ach}%' for cat, ach in zip(categories, achievements)], 
    colors=colors,
    autopct='%1.1f%%',  # Add percentage inside the pie slices
    startangle=90,      # Start the first slice at the top
    pctdistance=0.85    # Position of percentage labels
)

plt.title('CrowdNest Project Achievements', fontsize=15, fontweight='bold')

# Add a legend
plt.legend(
    [f'{cat}: {ach}%' for cat, ach in zip(categories, achievements)], 
    title='Components', 
    loc='center left', 
    bbox_to_anchor=(1, 0.5)
)

plt.tight_layout()
plt.savefig('c:\\Users\\dhana\\Downloads\\sem4mini\\CrowdNest--Collective-Resourse-Gathering-System\\achievement_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print("Achievement chart has been saved as achievement_chart.png")
