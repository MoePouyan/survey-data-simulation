# Survey Data Analysis Demo

This file serves as a placeholder for a Jupyter notebook that would demonstrate analysis of the simulated survey data. Below is an outline of the analysis that would be performed in a proper Jupyter notebook.

## 1. Loading and Exploring the Dataset

```python
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the simulated dataset
df = pd.read_csv("../data/simulated_survey_data.csv")

# Display basic information about the dataset
print(f"Dataset shape: {df.shape}")
df.head()

# Summary statistics
df.describe()

# Visualize age group distribution
plt.figure(figsize=(10, 6))
df['A3_age'].value_counts(normalize=True).sort_index().plot(kind='bar')
plt.title('Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Proportion')
plt.xticks(rotation=0)
plt.show()

# Visualize provincial distribution
plt.figure(figsize=(12, 6))
df['A4_province'].value_counts(normalize=True).sort_values().plot(kind='barh')
plt.title('Provincial Distribution')
plt.xlabel('Proportion')
plt.ylabel('Province')
plt.tight_layout()
plt.show()

# Filter for completed surveys only
completed = df[df['Completed'] == 1]

# Compare brand metrics between exposed and control groups
metrics = ['B3_Familiarity_BrandX', 'B4_Consideration_BrandX', 'B5_Recommendation_BrandX']

for metric in metrics:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Exposed_Flag', y=metric, data=completed)
    plt.title(f'{metric} by Exposure Group')
    plt.xlabel('Exposed to Advertisement (1=Yes, 0=No)')
    plt.ylabel('Rating')
    plt.show()
    
    # Calculate mean difference
    mean_exposed = completed[completed['Exposed_Flag']==1][metric].mean()
    mean_control = completed[completed['Exposed_Flag']==0][metric].mean()
    print(f"Mean {metric}: Exposed={mean_exposed:.2f}, Control={mean_control:.2f}, Lift={mean_exposed-mean_control:.2f}")

# Create a correlation matrix of key variables
corr_vars = ['Exposed_Flag', 'B3_Familiarity_BrandX', 'B4_Consideration_BrandX', 
             'B5_Recommendation_BrandX', 'A3_age', 'A2_gender']
             
corr_matrix = completed[corr_vars].corr()

# Visualize correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix of Key Variables')
plt.tight_layout()
plt.show()

# Filter for exposed respondents only
exposed = completed[completed['Exposed_Flag'] == 1]

# Analyze ad recall rates
recall_counts = exposed['C1_Ad_Recall_Pre'].value_counts(normalize=True)
plt.figure(figsize=(8, 6))
recall_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Ad Recall Rates Among Exposed Group')
plt.ylabel('')
plt.show()

# Compare brand metrics by recall status
recall_analysis = exposed.groupby('C1_Ad_Recall_Pre')[metrics].mean().reset_index()
print("Brand metrics by recall status:")
print(recall_analysis)
