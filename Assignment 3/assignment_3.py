# -*- coding: utf-8 -*-
"""Assignment_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19IrJWYoashdf9JxcEerfPue2CF879S-d
"""

# Importing relavent Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Plot style
sns.set(style='whitegrid', context='notebook', rc={'figure.figsize':(14,10)})

# Input Data and the cell/tissue location
df = pd.read_csv("C:\\Users\\shree\\Desktop\\Academics\\AIBD\\Assignment 3\\Dataset.csv", index_col=0).T.reset_index()
names = pd.read_csv("C:\\Users\\shree\\Desktop\\Academics\\AIBD\\Assignment 3\\Metadata_bt.csv")

df = df.rename(columns={'index': 'Genes'})
df["Genes"] = [gene.split(".ba")[0] for gene in df['Genes']]

names_dict = dict(zip(names['Sample'], names['Cell line/Tissue']))
df['Genes'] = [names_dict[gene] for gene in df['Genes']]

df

# Scale with mean = 0 and std deviation not set to 1
scaled_data = StandardScaler(with_mean=True, with_std=True).fit_transform(df[df.columns[1:]])

# PCA with 20 components
pca = PCA(n_components=20)
transformed_data = pca.fit_transform(scaled_data)
PCA_components = pca.components_

#Scree Plot + Histograms
PC_values = np.arange(pca.n_components_)
plt.plot(PC_values, pca.explained_variance_ratio_*100, 'o-', linewidth=2, color='blue')
sns.barplot(y = pca.explained_variance_ratio_*100,x = [f'Component {i}' for i in range(20)])
plt.xticks(rotation=45)
plt.title('Explained variance of the components', size=18)
plt.xlabel('Components', size=15)
plt.ylabel('Percentage of Explained Variance', size=15)
# plt.savefig('screeplot.svg')
plt.show()

# Plotting PC1 and PC2
transformed_df = pd.DataFrame(data = transformed_data, columns=[f'Component_{i}' for i in range(20)])
transformed_df['Genes'] = df['Genes']

fig, ax = plt.subplots(figsize=(10,10))
sns.scatterplot(data = transformed_df,x='Component_0',y='Component_1',hue = 'Genes',s=100)
ax.set_xlabel(f"PC1 - {pca.explained_variance_ratio_[0]*100:.2f}%")
ax.set_ylabel(f"PC2 - {pca.explained_variance_ratio_[1]*100:.2f}%")
ax.set_title("PC1 vs PC2")
# plt.savefig('PC1 vs PC2.svg')
plt.show()

# Identifying the top contributers for PC1 and PC2
PC1 = np.array(list(pca.components_[0]))
PC2 = np.array(list(pca.components_[1]))

sort_idx_1 = np.argsort(PC1)
PC1_sorted = PC1[sort_idx_1]
top5_1 = list(PC1_sorted[-5 : ])

for i in range(4,-1,-1):
    max_index = int(np.where(PC1 == top5_1[i])[0])
    gene_PC = df.columns[max_index+1]
    print(f'{4-i+1} most contributing gene in PC1 is {gene_PC}: {round(top5_1[i],6)}')

print('------------------------')
sort_idx_2 = np.argsort(PC2)
PC2_sorted = PC2[sort_idx_2]
top5_2 = list(PC2_sorted[-5 : ])

for i in range(4,-1,-1):
    max_index = int(np.where(PC2 == top5_2[i])[0])
    gene_PC = df.columns[max_index+1]
    print(f'{4-i+1} most contributing gene in PC2 is {gene_PC}: {round(top5_2[i],6)}')